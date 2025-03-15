import os
import shutil
import datetime
import mysql.connector
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, DATETIME

# Define the schema for indexing
schema = Schema(
    filename=TEXT(stored=True),
    filepath=ID(stored=True, unique=True),
    content_preview=TEXT(stored=True),
    filetype=TEXT(stored=True),
    modification_date=DATETIME(stored=True)
)

# Function to create or open the index
def create_or_open_index(index_dir):
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
        return create_in(index_dir, schema)
    else:
        return open_dir(index_dir)

# Fetch file metadata from the MySQL database
def get_files_from_db():
    db_config = {
        "host": "localhost",
    "user": "root",  # Change this to your MySQL username
    "password": "1900340220",  # Change this to your MySQL password
    "database": "file_monitor"  # Change this to your MySQL database name
    }
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, path, modification_time FROM txt_files_view")
    files = cursor.fetchall()
    
    conn.close()
    return files

# Index a single file
def index_file(index_dir, filename, filepath, modification_date):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        content_preview = content[:200]  # Store only a snippet

        # Open writer and update index
        ix = open_dir(index_dir)
        writer = ix.writer()
        writer.update_document(
            filename=filename,
            filepath=filepath,
            content_preview=content_preview,
            filetype=os.path.splitext(filepath)[1],
            modification_date=datetime.datetime.fromtimestamp(modification_date)
        )
        writer.commit()

        print(f"Indexed: {filepath}")

    except Exception as e:
        print(f"Error indexing {filepath}: {e}")

# Remove deleted files from index
def remove_deleted_files(index_dir):
    ix = open_dir(index_dir)
    writer = ix.writer()
    
    for root, _, files in os.walk(index_dir, followlinks=True):
        for file in files:
            filepath = os.path.join(root, file)
            if not os.path.exists(filepath):
                writer.delete_by_term("filepath", filepath)
                print(f"Removed from index: {filepath}")

    writer.commit()

# Index all files
def index_files(file_records, index_dir):
    create_or_open_index(index_dir)
    
    for filename, filepath, modification_date in file_records:
        index_file(index_dir, filename, filepath, modification_date)

    # Handle deletions
    remove_deleted_files(index_dir)
    
    print("Indexing completed.")

# Main execution
if __name__ == "__main__":
    index_directory = "./textindex"

    # Clear existing index directory if it exists
    if os.path.exists(index_directory):
        shutil.rmtree(index_directory)

    # Fetch file paths from the database
    file_records = get_files_from_db()

    # Recreate the index and index files
    index_files(file_records, index_directory)
