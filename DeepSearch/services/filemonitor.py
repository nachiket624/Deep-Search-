import os
import time
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dbconnection.db_utils import create_database_if_not_exists,create_table,ALLOWED_EXTENSIONS,get_db_connection,formatdate


logging.basicConfig(
    filename='deepsearchapp.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

class FileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            update_file_record(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")
            update_file_record(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"File deleted: {event.src_path}")
            update_file_record(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            logging.info(f"File moved from {event.src_path} to {event.dest_path}")
            update_file_record(event.dest_path)
            update_file_record(event.src_path)

def main():
    directory = input("Enter the directory path to monitor: ")
    if not os.path.isdir(directory):
        logging.error(f"Invalid directory path entered: {directory}")
        return
    create_database_if_not_exists()
    create_table()
    logging.info(f"Monitoring started on: {directory}")
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Monitoring stopped by user.")
    except Exception as e:
        logging.exception("Unexpected error occurred in observer loop.")
    observer.join()

if __name__ == "__main__":
    main()
