import os
import shutil
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from concurrent.futures import ThreadPoolExecutor

# Define the schema for indexing
schema = Schema(filepath=ID(stored=True, unique=True), content=TEXT(stored=True))

# Function to create or open the index
def create_or_open_index(index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        return create_in(index_dir, schema)
    else:
        return open_dir(index_dir)

# Function to index a single file
def index_file(writer, filepath):
    print(f"Indexing: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            writer.add_document(filepath=filepath, content=content)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

# Function to index all text files in a directory using multithreading
def index_files(directory, index_dir):
    """Indexes all .txt files in the specified directory using multithreading."""
    # Create or open the index
    index = create_or_open_index(index_dir)

    # Create a writer for the index
    writer = index.writer()

    # Collect all .txt file paths
    filepaths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                filepaths.append(os.path.join(root, file))

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=4) as executor:
        for filepath in filepaths:
            executor.submit(index_file, writer, filepath)

    # Commit changes to the index
    writer.commit()
    print("Indexing completed.")

# Main execution
if __name__ == "__main__":
    # Define paths
    text_files_directory = "../test/output_txt_files"  # Replace with your text files directory
    index_directory = "../Indexrecord/textindex"  # Directory to store the index

    # Clear existing index directory if it exists
    if os.path.exists(index_directory):
        shutil.rmtree(index_directory)

    # Recreate the index and index files
    index_files(text_files_directory, index_directory)