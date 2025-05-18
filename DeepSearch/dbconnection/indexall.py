import os
from datetime import datetime
import psutil
from db_utils import create_table, ALLOWED_EXTENSIONS, db_connection

def normalize_path(filepath):
    """Normalizes and sanitizes file paths."""
    return os.path.normpath(filepath).lower().strip()

def scan_directory(directory):
    """Scans the directory and updates the database with allowed files."""
    conn = db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()

    for root, _, files in os.walk(directory):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in ALLOWED_EXTENSIONS:
                filepath = normalize_path(os.path.join(root, file))
                try:
                    modification_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                    size = os.path.getsize(filepath)
                except Exception as e:
                    print(f"Error accessing {filepath}: {e}")
                    continue
                print(file, filepath, file_extension, modification_time, size)
                # Insert new record without deleting existing ones
                cursor.execute("""
                    INSERT INTO files (name, path, type, modification_time, size)
                    VALUES (?, ?, ?, ?, ?)
                """, (file, filepath, file_extension, modification_time, size))

    conn.commit()
    conn.close()


def get_internal_drives():
    """Returns a list of available internal disk drive paths."""
    drives = []
    for part in psutil.disk_partitions(all=False):
        if 'cdrom' in part.opts or part.fstype == '':
            continue
        if os.name == 'nt' and part.device[0].isalpha() and part.device[1:3] == ':\\':
            drives.append(part.mountpoint)
        elif os.name != 'nt':
            drives.append(part.mountpoint)
    return drives


def main():
    """Main function to scan and index files on internal drives."""
    drives = get_internal_drives()
    if not drives:
        print("No internal drives found!")
        return

    create_table()  # Assuming this sets up your database schema

    for drive in drives:
        print(f"Scanning {drive} ...")
        scan_directory(drive)

    print("Indexing complete.")


if __name__ == "__main__":
    main()
