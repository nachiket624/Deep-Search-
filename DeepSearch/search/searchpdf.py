from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.writing import AsyncWriter
from dbconnection.db_utils import get_db_connection

def file_exists_in_db(filepath):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM files WHERE path = %s", (filepath,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"Database check error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def search_files(query_str):
    index_dir = r"./indexfiles/pdf_index"
    results_list = []

    try:
        ix = open_dir(index_dir)
        searcher = ix.searcher()
        writer = AsyncWriter(ix)
        query = QueryParser("content_preview", ix.schema).parse(query_str)
        results = searcher.search(query, limit=10)

        for result in results:
            filepath = result["filepath"]
            if file_exists_in_db(filepath):
                results_list.append([
                    result["filename"],
                    filepath,
                    result["content_preview"]
                ])
            else:
                writer.delete_by_term("filepath", filepath)
                print(f"Removed from index (not in DB): {filepath}")

        searcher.close()
        writer.commit()

    except Exception as e:
        print(f"Error during search: {e}")
    return results_list

