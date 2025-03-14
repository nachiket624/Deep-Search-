import os
import shutil
import datetime
import json
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, DATETIME
from concurrent.futures import ThreadPoolExecutor

# Define the schema for indexing
schema = Schema(
    filename=TEXT(stored=True),
    filepath=ID(stored=True, unique=True),
    content_preview=TEXT(stored=True),
    filetype=TEXT(stored=True),
    modification_date=DATETIME(stored=True)
)

metadata_file = "file_metadata.json"

# Function to create or open the index
def create_or_open_index(index_dir):
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
        return create_in(index_dir, schema)
    else:
        return open_dir(index_dir)

# Load existing metadata to track file changes
def load_metadata():
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            return json.load(f)
    return {}

# Save metadata after indexing
def save_metadata(metadata):
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

# Get file metadata
def get_file_metadata(filepath):
    filename = os.path.basename(filepath)
    filetype = os.path.splitext(filepath)[1]
    modification_date = os.path.getmtime(filepath)  # Get timestamp
    
    return filename, filetype, modification_date

# Index a single file
def index_file(index_dir, filepath, metadata):
    try:
        filename, filetype, modification_date = get_file_metadata(filepath)
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        content_preview = content[:200]  # Store only a snippet

        # Check if the file is modified or newly added
        if filepath in metadata and metadata[filepath]["modification_date"] == modification_date:
            return  # No changes detected, skip indexing

        # Open writer and update index
        ix = open_dir(index_dir)
        writer = ix.writer()
        writer.update_document(
            filename=filename,
            filepath=filepath,
            content_preview=content_preview,
            filetype=filetype,
            modification_date=datetime.datetime.fromtimestamp(modification_date)
        )
        writer.commit()

        # Update metadata
        metadata[filepath] = {
            "filename": filename,
            "filetype": filetype,
            "modification_date": modification_date
        }

        print(f"Indexed: {filepath}")

    except Exception as e:
        print(f"Error indexing {filepath}: {e}")

# Remove deleted files from index
def remove_deleted_files(index_dir, metadata):
    ix = open_dir(index_dir)
    writer = ix.writer()
    deleted_files = []

    for filepath in list(metadata.keys()):
        if not os.path.exists(filepath):  # File deleted
            writer.delete_by_term("filepath", filepath)
            deleted_files.append(filepath)

    writer.commit()

    # Remove deleted files from metadata
    for filepath in deleted_files:
        del metadata[filepath]
        print(f"Removed from index: {filepath}")

# Detect moved files and update their path in the index
def update_moved_files(index_dir, directory, metadata):
    existing_files = {}
    
    # Scan the directory to map filenames to paths
    for root, _, files in os.walk(directory, followlinks=True):
        for file in files:
            filepath = os.path.join(root, file)
            existing_files[file] = filepath  # Map filename to new path

    ix = open_dir(index_dir)
    writer = ix.writer()
    moved_files = []

    for old_path, file_data in list(metadata.items()):
        filename = file_data["filename"]
        
        if filename in existing_files and existing_files[filename] != old_path:
            new_path = existing_files[filename]
            print(f"File moved: {old_path} → {new_path}")

            # Update index with the new path
            with open(new_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            writer.update_document(
                filename=filename,
                filepath=new_path,
                content_preview=content[:200],
                filetype=file_data["filetype"],
                modification_date=datetime.datetime.fromtimestamp(file_data["modification_date"])
            )

            moved_files.append((old_path, new_path))

    writer.commit()

    # Update metadata
    for old_path, new_path in moved_files:
        metadata[new_path] = metadata.pop(old_path)

# Index all files
def index_files(directory, index_dir):
    index = create_or_open_index(index_dir)
    metadata = load_metadata()

    filepaths = []
    for root, _, files in os.walk(directory, followlinks=True):
        for file in files:
            if file.endswith('.txt'):
                filepaths.append(os.path.join(root, file))

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=4) as executor:
        for filepath in filepaths:
            executor.submit(index_file, index_dir, filepath, metadata)

    # Handle deletions and moved files
    remove_deleted_files(index_dir, metadata)
    update_moved_files(index_dir, directory, metadata)

    # Save updated metadata
    save_metadata(metadata)
    print("Indexing completed.")

# Main execution
if __name__ == "__main__":
    text_files_directory = "./test"  # Replace with your text files directory
    index_directory = "./textindex"

    # Clear existing index directory if it exists
    if os.path.exists(index_directory):
        shutil.rmtree(index_directory)

    # Recreate the index and index files
    index_files(text_files_directory, index_directory)
