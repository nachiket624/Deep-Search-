import os
import sys
from datetime import datetime
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from dbconnection.db_utils import create_database_if_not_exists,ALLOWED_EXTENSIONS,get_db_connection,create_table

def scan_directory(directory):
    """Scans the directory and updates the database with allowed files."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in ALLOWED_EXTENSIONS:
                filepath = os.path.join(root, file)
                modification_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                size = os.path.getsize(filepath)
                cursor.execute("""
                    INSERT INTO files (name, path, type, modification_time, size)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE name=%s, modification_time=%s, size=%s
                """, (file, filepath, file_extension, modification_time, size, file, modification_time, size))
    
    conn.commit()
    conn.close()

def check_existing_records():
    """Checks if existing database records match files on disk."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM files")
    records = cursor.fetchall()
    for record in records:
        filepath = record[0]
        if not os.path.exists(filepath):
            cursor.execute("DELETE FROM files WHERE path = %s", (filepath,))
        else:
            modification_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            size = os.path.getsize(filepath)
            cursor.execute("UPDATE files SET modification_time=%s, size=%s WHERE path=%s",
                           (modification_time, size, filepath))
    conn.commit()
    conn.close()

def main():
    directory = "C:/"
    if not os.path.isdir(directory):
        print("Invalid directory path!")
        return
    create_database_if_not_exists()
    create_table()
    scan_directory(directory)
    check_existing_records()
    print("Indexing complete.")

if __name__ == "__main__":
    main()
