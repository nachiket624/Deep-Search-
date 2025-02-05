from whoosh.qparser import QueryParser
from whoosh.index import open_dir

# Open the index directory
index = open_dir("../../Indexrecord/textindex")

def search_index(query_text):
    with index.searcher() as searcher:
        query = QueryParser("content", index.schema).parse(query_text)  # Parse the query
        results = searcher.search(query, limit=10)  # Limit to 10 results
        if results:
            print(f"Found {len(results)} result(s):\n")
            for result in results:
                # Safely retrieve stored fields
                filepath = result.get('filepath', 'Unknown')
                content = result.get('content', 'Content not stored')
                print(f"File: {filepath}\nContent Preview:\n{content[:500]}...\n")  # Show up to 500 characters
        else:
            print("No results found.")

# Example usage
search_index(r"['Health & Fitness']")


