import os
import shutil
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from concurrent.futures import ThreadPoolExecutor
from docx import Document

# Define the schema for indexing
docx_schema = Schema(filepath=ID(stored=True, unique=True), content=TEXT(stored=True))

# Function to create or open the index
def create_or_open_docx_index(index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        return create_in(index_dir, docx_schema)
    else:
        return open_dir(index_dir)

# Function to extract text from a .docx file
def extract_text_from_docx(filepath):
    try:
        doc = Document(filepath)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return ""

# Function to index a single .docx file
def index_docx_file(writer, filepath):
    print(f"Indexing: {filepath}")
    try:
        content = extract_text_from_docx(filepath)
        writer.add_document(filepath=filepath, content=content)
    except Exception as e:
        print(f"Error indexing {filepath}: {e}")

# Function to index all .docx files in a directory using multithreading
def index_docx_files(directory, index_dir):
    """Indexes all .docx files in the specified directory using multithreading."""
    # Create or open the index
    index = create_or_open_docx_index(index_dir)

    # Create a writer for the index
    writer = index.writer()

    # Collect all .docx file paths
    filepaths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.docx'):
                filepaths.append(os.path.join(root, file))

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=4) as executor:
        for filepath in filepaths:
            executor.submit(index_docx_file, writer, filepath)

    # Commit changes to the index
    writer.commit()
    print("Indexing completed.")

# Main execution
if __name__ == "__main__":
    # Define paths
    docx_files_directory = "../../../test/output_doc_files"  # Replace with your .docx files directory
    index_directory = "../../../Indexrecord/docxindex"  # Directory to store the index

    # Clear existing index directory if it exists
    if os.path.exists(index_directory):
        shutil.rmtree(index_directory)

    # Recreate the index and index .docx files
    index_docx_files(docx_files_directory, index_directory)
