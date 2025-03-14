import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from Mainwindow.MainWindow import Ui_MainWindow

# List of allowed file extensions
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac",
                      ".doc", ".docx", ".pdf", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".rtf",
                      ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp",
                      ".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".mpeg",
                      ".exe", ".bat", ".sh", ".app", ".msi",
                      ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"}

# List of ignored directories
IGNORED_DIRECTORIES = {os.path.abspath(r"C:/$Recycle.Bin/")}

def is_ignored(path):
    path = os.path.abspath(path)
    if any(path.startswith(ignored) for ignored in IGNORED_DIRECTORIES):
        return True
    if any(part.startswith(".") for part in path.split(os.sep)):
        return True
    return False

class FileActivityHandler(FileSystemEventHandler,QtWidgets.QMainWindow, Ui_MainWindow):
    def is_valid_file_or_folder(self, path):
        return not is_ignored(path) and (os.path.isdir(path) or any(path.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS))

    def get_file_info(self, path):
        try:
            size = os.path.getsize(path) if os.path.isfile(path) else 0
            mod_time = time.ctime(os.path.getmtime(path))
            file_type = "Directory" if os.path.isdir(path) else "File"
            return size, mod_time, file_type
        except Exception:
            return None, None, None

    def on_modified(self, event):
        if self.is_valid_file_or_folder(event.src_path):
            size, mod_time, file_type = self.get_file_info(event.src_path)
            self.data.append({"Name": os.path.basename(event.src_path), "Path": event.src_path, "Type": file_type, "Modification Time": mod_time, "Size (bytes)": size})
            self.update_table()

    def on_created(self, event):
        if self.is_valid_file_or_folder(event.src_path):
            size, mod_time, file_type = self.get_file_info(event.src_path)
            print(f'Created: {event.src_path}, Type: {file_type}, Size: {size} bytes, Modified Time: {mod_time}')

    def on_deleted(self, event):
        if self.is_valid_file_or_folder(event.src_path):
            print(f'Deleted: {event.src_path}')

    def on_moved(self, event):
        if self.is_valid_file_or_folder(event.dest_path):
            size, mod_time, file_type = self.get_file_info(event.dest_path)
            print(f'Moved: {event.src_path} -> {event.dest_path}, Type: {file_type}, Size: {size} bytes, Modified Time: {mod_time}')

if __name__ == "__main__":
    path = "C:/"  # Change to the directory you want to monitor
    event_handler = FileActivityHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
