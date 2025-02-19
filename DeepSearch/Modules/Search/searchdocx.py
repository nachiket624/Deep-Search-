import os
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search_docx_index(index_dir, search_query):
    """Searches the index for the given query."""
    if not os.path.exists(index_dir):
        print("Index directory does not exist.")
        return

    index = open_dir(index_dir)
    with index.searcher() as searcher:
        query = QueryParser("content", index.schema).parse(search_query)
        results = searcher.search(query)
        print(f"Found {len(results)} result(s):")
        for result in results:
            print(f"File: {result['filepath']}")

# Main execution
if __name__ == "__main__":
    # Define index directory
    index_directory = "../../Indexrecord/docxindex"  # Directory where the index is stored

    # Perform a search
    search_query = "publisher: Hachette Digital, Inc."  # Replace with your search query
    search_docx_index(index_directory, search_query)

