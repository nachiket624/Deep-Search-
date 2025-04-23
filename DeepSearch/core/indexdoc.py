import os
import textract
from docx import Document
import mysql.connector
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID
from dbconnection.db_utils import get_db_connection

# Reuse same schema as txt
schema = Schema(
    filename=TEXT(stored=True),
    filepath=ID(stored=True, unique=True),
    content_preview=TEXT(stored=True)
)

user_profile = os.environ.get("USERPROFILE", r"C:\Users\Default")
appdata_path = os.path.join(user_profile, "AppData")
index_dir = os.path.abspath(r"..\indexfiles\docx_index")

EXCLUDED_DIRS = [
    os.environ.get("ProgramFiles", r"C:\Program Files"),
    os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
    r"C:\Windows",
    r"C:\PerfLogs",
    index_dir,
    appdata_path
]

def get_excluded_dirs():
    return EXCLUDED_DIRS

def is_excluded_path(path):
    norm_path = os.path.abspath(os.path.normpath(path)).lower()
    return any(norm_path.startswith(ex.lower()) for ex in get_excluded_dirs())

def is_valid_doc_file(path):
    return path.lower().endswith(('.doc', '.docx')) and not is_excluded_path(path)

def extract_text_from_doc(path):
    try:
        if path.lower().endswith('.docx'):
            doc = Document(path)
            return '\n'.join([p.text for p in doc.paragraphs])
        elif path.lower().endswith('.doc'):
            return textract.process(path).decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"❌ Error reading {path}: {e}")
    return ""

def get_indexed_file_paths_from_whoosh(index_dir):
    paths = []
    if not os.path.exists(index_dir):
        print(f"⚠️ Index directory not found: {index_dir}")
        return paths

    try:
        ix = open_dir(index_dir)
        with ix.searcher() as searcher:
            for doc in searcher.all_documents():
                paths.append(doc['filepath'])
    except Exception as e:
        print(f"Error reading index: {e}")

    return paths

def index_doc_files_from_mysql():
    if os.path.exists(index_dir) and exists_in(index_dir):
        ix = open_dir(index_dir)
    else:
        os.makedirs(index_dir, exist_ok=True)
        ix = create_in(index_dir, schema)

    writer = ix.writer()

    try:
        conn = get_db_connection(use_database=True)
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT name, path FROM files WHERE type IN ('.doc', '.docx')")
        db_files = cursor.fetchall()

        existing_indexed_paths = set(get_indexed_file_paths_from_whoosh(index_dir))
        indexed_now = set()

        for (name, path) in db_files:
            try:
                if not is_valid_doc_file(path):
                    print(f"⛔ Skipping: {path}")
                    continue

                if not os.path.exists(path):
                    print(f"🗑️ File missing: {path}")
                    writer.delete_by_term("filepath", path)
                    continue

                content = extract_text_from_doc(path)
                preview = content[:1000]

                if path in existing_indexed_paths:
                    writer.update_document(
                        filename=name,
                        filepath=path,
                        content_preview=preview
                    )
                    print(f"🔁 Updated: {path}")
                else:
                    writer.add_document(
                        filename=name,
                        filepath=path,
                        content_preview=preview
                    )
                    print(f"➕ Indexed: {path}")

                indexed_now.add(path)

            except Exception as e:
                print(f"❌ Error indexing {path}: {e}")

        for path in existing_indexed_paths - indexed_now:
            print(f"🧹 Removing stale index entry: {path}")
            writer.delete_by_term("filepath", path)

        writer.commit()
        cursor.close()
        conn.close()
        print("✅ Doc indexing complete.")

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")

def add_doc_to_index(file_path):
    if not is_valid_doc_file(file_path):
        print(f"⛔ Invalid doc file: {file_path}")
        return

    content = extract_text_from_doc(file_path)
    preview = content[:1000]

    try:
        ix = open_dir(index_dir)
        writer = ix.writer()
        writer.add_document(
            filename=os.path.basename(file_path),
            filepath=file_path,
            content_preview=preview
        )
        writer.commit()
        print(f"✅ Added to index: {file_path}")
    except Exception as e:
        print(f"❌ Failed to add {file_path}: {e}")

def update_doc_in_index(file_path):
    if not is_valid_doc_file(file_path):
        print(f"⛔ Invalid doc file: {file_path}")
        return

    content = extract_text_from_doc(file_path)
    preview = content[:1000]

    try:
        ix = open_dir(index_dir)
        writer = ix.writer()
        writer.update_document(
            filename=os.path.basename(file_path),
            filepath=file_path,
            content_preview=preview
        )
        writer.commit()
        print(f"🔄 Updated index for: {file_path}")
    except Exception as e:
        print(f"❌ Failed to update {file_path}: {e}")

def remove_doc_from_index(file_path):
    if not is_valid_doc_file(file_path):
        print(f"⛔ Invalid doc file: {file_path}")
        return

    try:
        ix = open_dir(index_dir)
        writer = ix.writer()
        writer.delete_by_term('filepath', file_path)
        writer.commit()
        print(f"🗑️ Removed from index: {file_path}")
    except Exception as e:
        print(f"❌ Failed to remove {file_path}: {e}")

if __name__ == "__main__":
    # index_doc_files_from_mysql()
    file_path = r"C:\Users\nachi\Documents\Doc my name is nachiket id 9920.docx"
    add_doc_to_index(file_path)
    # update_doc_in_index(r"C:\Users\you\Documents\sample.doc")
    # remove_doc_from_index(r"C:\Users\you\Documents\sample.docx")
    pass
