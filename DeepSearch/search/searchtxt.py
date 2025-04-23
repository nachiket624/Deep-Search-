from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from dbconnection.db_utils import get_db_connection
import logging
logging.basicConfig(
    filename='searctext.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
def search_files(query_str):
    index_dir = r"./indexfiles/textindex"
    results_list = []

    try:
        ix = open_dir(index_dir)
        searcher = ix.searcher()
        writer = ix.writer()
        query = QueryParser("content_preview", ix.schema).parse(query_str)
        results = searcher.search(query, limit=10)

        conn = get_db_connection(use_database=True)
        if conn is None:
            print("❌ Failed to connect to the database.")
            return []

        cursor = conn.cursor()

        for result in results:
            filepath = result["filepath"]

            # Check if this file exists in the database
            cursor.execute("SELECT COUNT(*) FROM files WHERE path = %s", (filepath,))
            (count,) = cursor.fetchone()

            if count > 0:
                results_list.append([
                    result["filename"],
                    filepath,
                    result["content_preview"]
                ])
            else:
                # Remove from index if not in DB
                print(f"🗑️ Removing from index (not in DB): {filepath}")
                writer.delete_by_term('filepath', filepath)

        writer.commit()
        cursor.close()
        conn.close()
        searcher.close()

    except Exception as e:
        print(f"Error during search: {e}")
    return results_list

 # Return results as a list

# print(search_files("my name is nachiket id 9300"))