import os
import shutil
import mysql.connector
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from dbconnection.db_utils import get_db_connection


# Define Whoosh schema
schema = Schema(
    filename=TEXT(stored=True),
    filepath=ID(stored=True, unique=True),
    content_preview=TEXT(stored=True)
)

def index_txt_files_from_mysql():
    index_dir = r"..\indexfiles\textindex"

    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.mkdir(index_dir)
    ix = create_in(index_dir, schema)
    writer = ix.writer()

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
        cursor.execute("SELECT name, path FROM files WHERE type = '.txt'")

        for (name, path) in cursor.fetchall():
            try:
                norm_path = os.path.normpath(path).lower()
                if any(norm_path.startswith(ex_dir) for ex_dir in excluded_dirs):
                    print(f"⛔ Skipping system file: {path}")
                    continue

                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    preview = content[:1000]
                    writer.add_document(
                        filename=name,
                        filepath=path,
                        content_preview=preview
                    )
                    print(f"✅ Indexed: {path}")
            except Exception as file_error:
                print(f"❌ Could not read file {path}: {file_error}")

        cursor.close()
        conn.close()
        writer.commit()
        print("✅ Indexing completed.")

    except mysql.connector.Error as db_error:
        print(f"MySQL error: {db_error}")

def search_files(query_str):
    index_dir = "textindex"
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

def get_indexed_txt_file_paths_from_db():
    txt_paths = []

    try:
        conn = get_db_connection(use_database=True)
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute("SELECT path FROM files WHERE type = '.txt'")

        for (path,) in cursor.fetchall():
            txt_paths.append(path)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")

    return txt_paths

def get_indexed_file_paths_from_whoosh(index_dir="textindex"):
    indexed_paths = []

    try:
        ix = open_dir(index_dir)
        with ix.searcher() as searcher:
            for doc in searcher.all_documents():
                indexed_paths.append(doc['filepath'])

    except Exception as e:
        print(f"Error reading index: {e}")

    return indexed_paths

def compare_index_and_db():
    mysql_paths = set(get_indexed_txt_file_paths_from_db())
    whoosh_paths = set(get_indexed_file_paths_from_whoosh())

    missing_in_index = mysql_paths - whoosh_paths
    orphan_in_index = whoosh_paths - mysql_paths

    print("🔍 Files in DB but not indexed:")
    for path in missing_in_index:
        print(f"  - {path}")

    print("\n🧹 Files indexed but not in DB:")
    for path in orphan_in_index:
        print(f"  - {path}")

if __name__ == "__main__":
    # Step 1: Index files
    index_txt_files_from_mysql()

    # Step 2: Perform a test search
    print("\n🔎 Search Results for 'example':")
    results = search_files("example")
    for filename, filepath, preview in results:
        print(f"\n📄 {filename} ({filepath})\n{preview[:200]}...\n")

    # Step 3: Show all .txt paths from DB
    print("\n📁 Indexed Paths from DB:")
    for path in get_indexed_txt_file_paths_from_db():
        print(f" - {path}")

    # Step 4: Compare DB and Whoosh Index
    print("\n🔍 Compare DB and Index:")
    compare_index_and_db()