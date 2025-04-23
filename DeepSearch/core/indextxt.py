import os
import mysql.connector
from whoosh.index import create_in, open_dir,exists_in
from whoosh.fields import Schema, TEXT, ID
from dbconnection.db_utils import get_db_connection

# Define Whoosh schema
schema = Schema(
    filename=TEXT(stored=True),
    filepath=ID(stored=True, unique=True),
    content_preview=TEXT(stored=True)
)
user_profile = os.environ.get("USERPROFILE", r"C:\Users\Default")
appdata_path = os.path.join(user_profile, "AppData")
index_dir = r"..\indexfiles\textindex"
def get_excluded_dirs():
    dirs = [
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        r"C:\Windows",
        r"C:\PerfLogs",
        index_dir,  # root of index dir
        appdata_path
    ]
    return dirs

def is_excluded_path(path):
    norm_path = os.path.abspath(os.path.normpath(path)).lower()
    return any(norm_path.startswith(ex) for ex in get_excluded_dirs())



def index_txt_files_from_mysql():
    # Create or open index
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
        cursor.execute("SELECT name, path FROM files WHERE type = '.txt'")
        db_files = cursor.fetchall()

        # Get existing indexed paths
        existing_indexed_paths = set(get_indexed_file_paths_from_whoosh(index_dir))
        indexed_now = set()

        for (name, path) in db_files:
            try:
                if is_excluded_path(path):
                    print(f"⛔ Skipping excluded path: {path}")
                    continue

                if not os.path.exists(path):
                    print(f"🗑️ File missing on disk, removing from index: {path}")
                    writer.delete_by_term("filepath", path)
                    continue

                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
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

            except Exception as file_error:
                print(f"❌ Could not read file {path}: {file_error}")

        # Optionally remove obsolete paths still in index but not in DB
        for path in existing_indexed_paths - indexed_now:
            print(f"🧹 Removing obsolete index entry (not in DB): {path}")
            writer.delete_by_term("filepath", path)

        writer.commit()
        cursor.close()
        conn.close()
        print("✅ Indexing completed.")

    except mysql.connector.Error as db_error:
        print(f"MySQL error: {db_error}")
def get_indexed_txt_file_paths_from_db():
    txt_paths = []

    try:
        conn = get_db_connection(use_database=True)
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT path FROM files WHERE type = '.txt'")

        for (path,) in cursor.fetchall():
            txt_paths.append(path)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")

    return txt_paths

def get_indexed_file_paths_from_whoosh(index_dir):
    indexed_paths = []

    if not os.path.exists(index_dir):
        print(f"⚠️ Index directory not found: {index_dir}")
        return []

    try:
        ix = open_dir(index_dir)
        with ix.searcher() as searcher:
            for doc in searcher.all_documents():
                indexed_paths.append(doc['filepath'])

    except Exception as e:
        print(f"Error reading index: {e}")

    return indexed_paths



# --- NEW FILE OPERATIONS ---
def add_file_to_index(file_path):
    try:
        if not file_path.lower().endswith('.txt'):
            print(f"⛔ Skipping non-txt file: {file_path}")
            return

        if is_excluded_path(file_path):
            print(f"⛔ Skipping system file: {file_path}")
            return

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        ix = open_dir(index_dir)
        writer = ix.writer()
        writer.add_document(
            filename=os.path.basename(file_path),
            filepath=file_path,
            content_preview=content
        )
        writer.commit()
        print(f"✅ Added to index: {file_path}")
    except Exception as e:
        print(f"❌ Failed to add {file_path}: {e}")

def update_file_in_index(file_path, index_dir=r"..\indexfiles\textindex"):
    try:
        if not file_path.lower().endswith('.txt'):
            print(f"⛔ Skipping non-txt file: {file_path}")
            return

        if is_excluded_path(file_path):
            print(f"⛔ Skipping system file: {file_path}")
            return

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read(1000)

        ix = open_dir(index_dir)
        writer = ix.writer()
        writer.update_document(
            filename=os.path.basename(file_path),
            filepath=file_path,
            content_preview=content
        )
        writer.commit()
        print(f"🔄 Updated index for: {file_path}")
    except Exception as e:
        print(f"❌ Failed to update {file_path}: {e}")

def remove_file_from_index(file_path):
    try:
        if not file_path.lower().endswith('.txt'):
            print(f"⛔ Skipping non-txt file: {file_path}")
            return

        if is_excluded_path(file_path):
            print(f"⛔ Skipping excluded path (not removing): {file_path}")
            return

        ix = open_dir(index_dir)
        writer = ix.writer()
        writer.delete_by_term('filepath', file_path)
        writer.commit()
        print(f"🗑️ Removed from index: {file_path}")
    except Exception as e:
        print(f"❌ Failed to remove {file_path}: {e}")
