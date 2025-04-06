from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search_files(query_str):
    index_dir = r"../pdf_index" 
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
