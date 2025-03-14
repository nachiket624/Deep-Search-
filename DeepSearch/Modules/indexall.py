import os
import sqlite3
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define allowed file extensions
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac",
                      ".doc", ".docx", ".pdf", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".rtf",
                      ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp",
                      ".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".mpeg",
                      ".exe", ".bat", ".sh", ".app", ".msi",
                      ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"}

def create_database():
    """Creates an SQLite database and a table to store file details."""
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        path TEXT UNIQUE,
                        type TEXT,
                        modification_time REAL,
                        size INTEGER)''')
    conn.commit()
    conn.close()

def scan_directory(directory):
    """Scans the directory for allowed files and populates the database."""
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in ALLOWED_EXTENSIONS:
                filepath = os.path.join(root, file)
                modification_time = os.path.getmtime(filepath)
                size = os.path.getsize(filepath)
                cursor.execute("INSERT INTO files (name, path, type, modification_time, size) VALUES (?, ?, ?, ?, ?) ON CONFLICT(path) DO UPDATE SET name=?, modification_time=?, size=?",
                               (file, filepath, file_extension, modification_time, size, file, modification_time, size))
    
    conn.commit()
    conn.close()

def check_existing_records():
    """Checks if existing records in the database still match the file system."""
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM files")
    records = cursor.fetchall()
    for record in records:
        filepath = record[0]
        if not os.path.exists(filepath):
            cursor.execute("DELETE FROM files WHERE path = ?", (filepath,))
        else:
            modification_time = os.path.getmtime(filepath)
            size = os.path.getsize(filepath)
            cursor.execute("UPDATE files SET modification_time=?, size=? WHERE path=?",
                           (modification_time, size, filepath))
    conn.commit()
    conn.close()

def update_file_record(filepath):
    """Updates or inserts file records in the database."""
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()
    if os.path.exists(filepath):
        file = os.path.basename(filepath)
        file_extension = os.path.splitext(file)[1].lower()
        if file_extension in ALLOWED_EXTENSIONS:
            modification_time = os.path.getmtime(filepath)
            size = os.path.getsize(filepath)
            cursor.execute("INSERT INTO files (name, path, type, modification_time, size) VALUES (?, ?, ?, ?, ?) ON CONFLICT(path) DO UPDATE SET name=?, modification_time=?, size=?",
                           (file, filepath, file_extension, modification_time, size, file, modification_time, size))
    else:
        cursor.execute("DELETE FROM files WHERE path = ?", (filepath,))
    conn.commit()
    conn.close()

class FileEventHandler(FileSystemEventHandler):
    """Handles file system events in real-time."""
    def on_modified(self, event):
        if not event.is_directory:
            update_file_record(event.src_path)
    
    def on_created(self, event):
        if not event.is_directory:
            update_file_record(event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            update_file_record(event.src_path)
    
    def on_moved(self, event):
        if not event.is_directory:
            update_file_record(event.dest_path)
            update_file_record(event.src_path)

def main():
    directory = input("Enter the directory path to monitor: ")
    if not os.path.isdir(directory):
        print("Invalid directory path!")
        return
    create_database()
    scan_directory(directory)
    check_existing_records()
    print("Initial scan and database check complete. Now monitoring for changes...")
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Monitoring stopped.")

if __name__ == "__main__":
    main()