import os
import time
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil  # <-- NEW IMPORT

from dbconnection.db_utils import (
    create_database_if_not_exists,
    create_table,
    ALLOWED_EXTENSIONS,
    get_db_connection,
    formatdate
)
from core.indextxt import add_file_to_index as add_txt, update_file_in_index as update_txt, remove_file_from_index as remove_txt
from core.indexdoc import add_doc_to_index as add_doc, update_doc_in_index as update_doc, remove_doc_from_index as remove_doc
from core.indexpdf import add_pdf_to_index as add_pdf, update_pdf_in_index as update_pdf, remove_pdf_from_index as remove_pdf

# --- Log file maintenance ---
LOG_FILE = 'deepsearchapp.log'
MAX_LOG_SIZE_MB = 20

if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE_MB * 1024 * 1024:
    os.remove(LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- DB Update Function ---
def update_file_record(filepath):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if os.path.exists(filepath):
            file = os.path.basename(filepath)
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in ALLOWED_EXTENSIONS:
                modification_time = os.path.getmtime(filepath)
                modification_time = formatdate(modification_time)
                size = os.path.getsize(filepath)
                cursor.execute("""
                    INSERT INTO files (name, path, type, modification_time, size)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE name=%s, modification_time=%s, size=%s
                """, (file, filepath, file_extension, modification_time, size, file, modification_time, size))
                logging.info(f"Indexed/Updated: {filepath}")
        else:
            cursor.execute("DELETE FROM files WHERE path = %s", (filepath,))
            logging.info(f"Deleted from DB: {filepath}")
        conn.commit()
    except Exception as e:
        logging.exception(f"Error updating record for file: {filepath}")
    finally:
        if conn:
            conn.close()

# --- File Indexing Dispatcher ---
def handle_indexing(file_path, action):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        if action == "add":
            add_txt(file_path)
        elif action == "update":
            update_txt(file_path)
        elif action == "remove":
            remove_txt(file_path)
    elif ext in [".doc", ".docx"]:
        if action == "add":
            add_doc(file_path)
        elif action == "update":
            update_doc(file_path)
        elif action == "remove":
            remove_doc(file_path)
    elif ext == ".pdf":
        if action == "add":
            add_pdf(file_path)
        elif action == "update":
            update_pdf(file_path)
        elif action == "remove":
            remove_pdf(file_path)

# --- Watchdog Event Handler ---
class FileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            update_file_record(event.src_path)
            handle_indexing(event.src_path, "update")

    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")
            update_file_record(event.src_path)
            handle_indexing(event.src_path, "add")

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"File deleted: {event.src_path}")
            update_file_record(event.src_path)
            handle_indexing(event.src_path, "remove")

    def on_moved(self, event):
        if not event.is_directory:
            logging.info(f"File moved from {event.src_path} to {event.dest_path}")
            handle_indexing(event.src_path, "remove")
            update_file_record(event.dest_path)
            handle_indexing(event.dest_path, "add")

# --- Get Internal Drives ---
def get_internal_drives():
    drives = []
    partitions = psutil.disk_partitions(all=False)
    for p in partitions:
        if ('fixed' in p.opts.lower() or p.fstype) and os.path.isdir(p.mountpoint):
            drives.append(p.mountpoint)
    return drives

# --- Main Function ---
def main():
    drives = get_internal_drives()
    if not drives:
        logging.error("No valid internal drives found to monitor.")
        return

    create_database_if_not_exists()
    create_table()

    observers = []
    for drive in drives:
        logging.info(f"Monitoring started on: {drive}")
        event_handler = FileEventHandler()
        observer = Observer()
        observer.schedule(event_handler, drive, recursive=True)
        observer.start()
        observers.append(observer)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        logging.info("Monitoring stopped by user.")
    except Exception as e:
        logging.exception("Unexpected error occurred in observer loop.")
    finally:
        for observer in observers:
            observer.join()

if __name__ == "__main__":
    main()
