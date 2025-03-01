import json
import os
from datetime import datetime

def load_index(file_path):
    """Load file index from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: file_index.json not found.")
        return []

def search_files(index, name=None, file_type=None, mod_date=None, size=None):
    """Search for files based on given criteria."""
    results = []
    for entry in index:
        if name and name.lower() not in entry["Name"].lower():
            continue
        if file_type and not entry["Name"].lower().endswith(file_type.lower()):
            continue
        if mod_date:
            entry_mod_time = datetime.strptime(entry["Modification Time"], "%a %b %d %H:%M:%S %Y")
            if mod_date != entry_mod_time.strftime("%Y-%m-%d"):
                continue
        if size and entry["Size (bytes)"] != "N/A":
            try:
                if int(entry["Size (bytes)"]) != size:
                    continue
            except ValueError:
                pass
        results.append(entry)
    return results

def main():
    file_index = load_index(r"DeepSearch\Modules\Indexrecord\file_index.json")
    if not file_index:
        return
    
    print("Search files by name, type, modification date (YYYY-MM-DD), or size.")
    name = input("Enter file name (or part of it, leave blank to skip): ")
    file_type = input("Enter file extension (e.g., .txt, .pdf, leave blank to skip): ")
    mod_date = input("Enter modification date (YYYY-MM-DD, leave blank to skip): ")
    size = input("Enter file size in bytes (leave blank to skip): ")
    
    size = int(size) if size.isdigit() else None
    results = search_files(file_index, name, file_type, mod_date, size)
    
    if results:
        print("\nSearch Results:")
        for res in results:
            print(json.dumps(res, indent=4))
    else:
        print("No matching files found.")

if __name__ == "__main__":
    main()
