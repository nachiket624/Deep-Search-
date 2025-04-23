import os
import shutil
import mysql.connector
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from docx import Document
from dbconnection.db_utils import get_db_connection

# Whoosh schema
schema = Schema(
    filename=TEXT(stored=True),
    filepath=ID(stored=True, unique=True),
    content_preview=TEXT(stored=True)
)

# Function to extract text from .docx
def extract_docx_text(path):
    try:
        doc = Document(path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"⚠️ Error reading {path}: {e}")
        return ""

# Index .docx files from MySQL
def index_docx_files_from_mysql():
    index_dir = "docx_index"

    # Reset index
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.mkdir(index_dir)

    # Create Whoosh index
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    # System folders to skip
    excluded_dirs = [
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        r"C:\Windows",
        r"C:\PerfLogs"
    ]
    excluded_dirs = [os.path.normpath(p).lower() for p in excluded_dirs]

    try:
        conn = get_db_connection(use_database=False)
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute("SELECT name, path FROM files WHERE type = '.docx'")

        for (name, path) in cursor.fetchall():
            try:
                norm_path = os.path.normpath(path).lower()
                if any(norm_path.startswith(ex_dir) for ex_dir in excluded_dirs):
                    print(f"⛔ Skipping system file: {path}")
                    continue

                content = extract_docx_text(path)
                if content.strip():
                    preview = content[:1000]
                    writer.add_document(
                        filename=name,
                        filepath=path,
                        content_preview=preview
                    )
                    print(f"✅ Indexed: {path}")
                else:
                    print(f"⚠️ Empty or unreadable: {path}")
            except Exception as file_error:
                print(f"❌ Could not process file {path}: {file_error}")

        cursor.close()
        conn.close()
        writer.commit()
        print("✅ Indexing of DOCX files completed.")

    except mysql.connector.Error as db_error:
        print(f"MySQL error: {db_error}")

# Search Whoosh index
def search_docx(query_str):
    index_dir = "docx_index"
    results_list = []

    try:
        ix = open_dir(index_dir)
        with ix.searcher() as searcher:
            query = QueryParser("content_preview", ix.schema).parse(query_str)
            results = searcher.search(query, limit=10)

            for result in results:
                results_list.append([
                    result["filename"],
                    result["filepath"],
                    result["content_preview"]
                ])
    except Exception as e:
        print(f"Error during search: {e}")

    return results_list

# Run everything
if __name__ == "__main__":
    index_docx_files_from_mysql()

    print("\n🔎 Search Results for 'invoice':")
    results = search_docx("invoice")
    for filename, filepath, preview in results:
        print(f"\n📄 {filename} ({filepath})\n{preview[:200]}...\n")
