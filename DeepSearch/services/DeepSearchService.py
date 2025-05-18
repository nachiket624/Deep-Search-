import os
import sys
import time
import logging
import psutil
import servicemanager
import threading
import win32serviceutil
import win32service
import win32event
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Fix imports ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

try:
    from dbconnection.db_utils import (
        create_database_if_not_exists,
        create_table,
        ALLOWED_EXTENSIONS,
        get_db_connection,
        formatdate
    )
except ModuleNotFoundError as e:
    servicemanager.LogErrorMsg(f"Import error: {str(e)}")
    raise

from core.indextxt import add_file_to_index as add_txt, update_file_in_index as update_txt, remove_file_from_index as remove_txt
from core.indexdoc import add_doc_to_index as add_doc, update_doc_in_index as update_doc, remove_doc_from_index as remove_doc
from core.indexpdf import add_pdf_to_index as add_pdf, update_pdf_in_index as update_pdf, remove_pdf_from_index as remove_pdf

# --- Logging Setup ---
LOG_FILE = 'deepsearchapp.log'
MAX_LOG_SIZE_MB = 20

if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE_MB * 1024 * 1024:
    os.remove(LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- File update functions ---
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

# --- File System Event Handler ---
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

# --- Helper to find drives ---
def get_internal_drives():
    drives = []
    partitions = psutil.disk_partitions(all=False)
    for p in partitions:
        if ('fixed' in p.opts.lower() or p.fstype) and os.path.isdir(p.mountpoint):
            drives.append(p.mountpoint)
    return drives

# --- Windows Service Class ---
class DeepSearchService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DeepSearchFileMonitor"
    _svc_display_name_ = "Deep Search File Monitor Service"
    _svc_description_ = "Monitors internal drives for file changes and updates the search index and database."

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.observers = []

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.stop_event)
        for observer in self.observers:
            observer.stop()
        for observer in self.observers:
            observer.join()
        logging.info("Service stopped successfully.")

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        logging.info("Service is starting...")

        # Start monitoring with timeout
        monitor_thread = threading.Thread(target=self.start_monitoring)
        monitor_thread.start()

        # Wait max 25 seconds for monitoring initialization
        monitor_thread.join(25)

        if monitor_thread.is_alive():
            logging.error("Monitoring initialization timed out")
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
            return

        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        logging.info("Service started successfully.")

        # Wait until stop event is triggered
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def start_monitoring(self):
        try:
            create_database_if_not_exists()
            create_table()

            drives = get_internal_drives()
            event_handler = FileEventHandler()

            for drive in drives:
                observer = Observer()
                observer.schedule(event_handler, drive, recursive=True)
                observer.start()
                self.observers.append(observer)
                logging.info(f"Monitoring drive: {drive}")

            logging.info("Monitoring started on all internal drives.")
            return True
        except Exception as e:
            logging.exception(f"Error in start_monitoring: {e}")
            return False

        while self.running:
            time.sleep(1)

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(DeepSearchService)
