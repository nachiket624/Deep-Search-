from whoosh.qparser import QueryParser
from whoosh.index import open_dir

# Open the index directory
index_path = "C:/Users/nachi/Documents/deep Search/DeepSearch/Modules/Indexrecord/textindex"

try:
    index = open_dir(index_path)
except Exception as e:
    print(f"Error opening index: {e}")
    exit()

def search_index(query_text):
    try:
        with index.searcher() as searcher:
            query = QueryParser("content", index.schema).parse(query_text)  # Parse the query
            results = searcher.search(query, limit=10)  # Limit to 10 results
            
            if results:
                print(f"\nFound {len(results)} result(s):\n")
                result_list = []
                for i, result in enumerate(results, 1):
                    filepath = result.get("filepath", "Unknown")
                    content = result.get("content", "Content not stored")

                    result_list.append([
                        i,  # Index
                        filepath,  # File Path
                        content[:500]  # Content Preview (first 500 characters)
                    ])
                
                return result_list  # ✅ Return as a list of lists
            
            else:
                print("No results found.")
                return []  # Return an empty list if no results are found

    except Exception as e:
        print(f"Error during search: {e}")
        return []  # Return an empty list on error

# search_index("It is a long established fact that a reader will be distracted by the readable")
