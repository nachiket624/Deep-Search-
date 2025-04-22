from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search_files(query_str):
    index_dir = r"./indexfiles/docx_index" 
    results_list = []

    try:
        ix = open_dir(index_dir)
        searcher = ix.searcher()
        query = QueryParser("content_preview", ix.schema).parse(query_str)
        results = searcher.search(query, limit=10)
        
        for result in results:
            results_list.append([
                result["filename"],
                result["filepath"],
                result["content_preview"]
            ])
        
        searcher.close()
    
    except Exception as e:
        print(f"Error during search: {e}")
    return results_list # Return results as a list


# Main execution
if __name__ == "__main__":
    # Define index directory
    index_directory = "../../Indexrecord/docxindex"  # Directory where the index is stored

    # Perform a search
    search_query = "publisher: Hachette Digital, Inc."  # Replace with your search query
    search_files(search_query)

