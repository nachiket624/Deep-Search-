from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from dbconnection.db_utils import get_db_connection
import logging

logging.basicConfig(
    filename='searchdocx.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def search_files(query_str):
    index_dir = r"./indexfiles/docx_index"
    results_list = []

    try:
        ix = open_dir(index_dir)
        searcher = ix.searcher()
        query = QueryParser("content_preview", ix.schema).parse(query_str)
        results = searcher.search(query, limit=10)

        conn = get_db_connection(use_database=True)
        if conn is None:
            print("❌ Failed to connect to the database.")
            searcher.close()
            return []

        cursor = conn.cursor()
        stale_filepaths = []

        for result in results:
            filepath = result["filepath"]

            cursor.execute("SELECT COUNT(*) FROM files WHERE path = %s", (filepath,))
            (count,) = cursor.fetchone()

            if count > 0:
                results_list.append([
                    result["filename"],
                    filepath,
                    result["content_preview"]
                ])
            else:
                stale_filepaths.append(filepath)

        searcher.close()
        cursor.close()
        conn.close()

        # Delete stale entries after closing searcher
        if stale_filepaths:
            writer = ix.writer()
            for path in stale_filepaths:
                writer.delete_by_term('filepath', path)
            writer.commit()

    except Exception as e:
        logging.error(f"Error during .docx search: {e}")
        print(f"⚠️ Error during search: {e}")

    return results_list
