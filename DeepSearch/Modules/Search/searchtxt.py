from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search_files(index_dir, query_str):
    try:
        ix = open_dir(index_dir)
        searcher = ix.searcher()
        query = QueryParser("content_preview", ix.schema).parse(query_str)
        results = searcher.search(query, limit=10)
        
        print(f"Found {len(results)} result(s):")
        for result in results:
            print(f"Filename: {result['filename']}")
            print(f"Filepath: {result['filepath']}")
            print(f"Snippet: {result['content_preview']}")
            print("-" * 50)
        
        searcher.close()
    except Exception as e:
        print(f"Error during search: {e}")

# Main execution
if __name__ == "__main__":
    index_directory = r"./textindex"  # Ensure this matches your indexing script
    search_query = "Eothen is the earliest work of Alexander William Kinglake"
    search_files(index_directory, search_query)