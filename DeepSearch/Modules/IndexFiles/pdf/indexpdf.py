import os
import shutil
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from concurrent.futures import ThreadPoolExecutor
from PyPDF2 import PdfReader

# Define the schema for indexing
pdf_schema = Schema(filepath=ID(stored=True, unique=True), content=TEXT(stored=True))

# Function to create or open the index
def create_or_open_pdf_index(index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        return create_in(index_dir, pdf_schema)
    else:
        return open_dir(index_dir)

# Function to extract text from a PDF file
def extract_text_from_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return ""

# Function to index a single PDF file
def index_pdf_file(writer, filepath):
    print(f"Indexing: {filepath}")
    try:
        content = extract_text_from_pdf(filepath)
        writer.add_document(filepath=filepath, content=content)
    except Exception as e:
        print(f"Error indexing {filepath}: {e}")

# Function to index all PDF files in a directory using multithreading
def index_pdf_files(directory, index_dir):
    """Indexes all PDF files in the specified directory using multithreading."""
    # Create or open the index
    index = create_or_open_pdf_index(index_dir)

    # Create a writer for the index
    writer = index.writer()

    # Collect all PDF file paths
    filepaths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                filepaths.append(os.path.join(root, file))

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=4) as executor:
        for filepath in filepaths:
            executor.submit(index_pdf_file, writer, filepath)

    # Commit changes to the index
    writer.commit()
    print("Indexing completed.")

# Main execution
if __name__ == "__main__":
    # Define paths
    pdf_files_directory = "output_pdf_files"  # Replace with your PDF files directory
    index_directory = "pdf_indexdir"  # Directory to store the index

    # Clear existing index directory if it exists
    if os.path.exists(index_directory):
        shutil.rmtree(index_directory)

    # Recreate the index and index PDF files
    index_pdf_files(pdf_files_directory, index_directory)
