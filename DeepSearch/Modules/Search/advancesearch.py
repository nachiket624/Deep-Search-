import json
import os
from datetime import datetime
import unicodedata

def load_index(file_path):
    """Load file index from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: file_index.json not found.")
        return []

def normalize_string(s):
    """Normalize string to remove diacritics."""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def search_files(index, name=None, file_type=None, mod_date=None, size=None, date_range=None, size_range=None, match_case=False, match_whole_word=False, match_diacritics=False):
    """Search for files based on given criteria."""
    print("search_files called")
    results = []
    for entry in index:
        file_name = entry["Name"]
        if not match_case:
            file_name = file_name.lower()
            if name:
                name = name.lower()
        if not match_diacritics and name:
            file_name = normalize_string(file_name)
            name = normalize_string(name)
        if name:
            if match_whole_word:
                if file_name != name:
                    continue
            else:
                if name not in file_name:
                    continue
        if file_type and not entry["Name"].lower().endswith(file_type.lower()):
            continue
        if mod_date:
            entry_mod_time = datetime.strptime(entry["Modification Time"], "%a %b %d %H:%M:%S %Y")
            if mod_date != entry_mod_time.strftime("%Y-%m-%d"):
                continue
        if date_range:
            start_date, end_date = date_range
            entry_mod_time = datetime.strptime(entry["Modification Time"], "%a %b %d %H:%M:%S %Y")
            if not (start_date <= entry_mod_time.date() <= end_date):
                continue
        if size and entry["Size (bytes)"] != "N/A":
            try:
                if int(entry["Size (bytes)"]) != size:
                    continue
            except ValueError:
                pass
        if size_range and entry["Size (bytes)"] != "N/A":
            try:
                file_size = int(entry["Size (bytes)"])
                if not (size_range[0] <= file_size <= size_range[1]):
                    continue
            except ValueError:
                pass
        results.append(entry)
    return results

def main():
    file_index = load_index(r"DeepSearch\Modules\Indexrecord\file_index.json")
    if not file_index:
        return
    
    print("Search files by name, type, modification date (YYYY-MM-DD), date range (YYYY-MM-DD to YYYY-MM-DD), size, or size range.")
    name = input("Enter file name (or part of it, leave blank to skip): ")
    file_type = input("Enter file extension (e.g., .txt, .pdf, leave blank to skip): ")
    mod_date = input("Enter modification date (YYYY-MM-DD, leave blank to skip): ")
    date_range_input = input("Enter date range (YYYY-MM-DD to YYYY-MM-DD, leave blank to skip): ")
    size = input("Enter file size in bytes (leave blank to skip): ")
    size_range_input = input("Enter size range (min-max bytes, leave blank to skip): ")
    match_case = input("Match case? (yes/no): ").strip().lower() == "yes"
    match_whole_word = input("Match whole word? (yes/no): ").strip().lower() == "yes"
    match_diacritics = input("Match diacritics? (yes/no): ").strip().lower() == "yes"
    
    size = int(size) if size.isdigit() else None
    date_range = None
    size_range = None
    
    if date_range_input:
        try:
            start_str, end_str = date_range_input.split(" to ")
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
            date_range = (start_date, end_date)
        except ValueError:
            print("Invalid date range format.")
            return
    
    if size_range_input:
        try:
            min_size, max_size = map(int, size_range_input.split("-"))
            size_range = (min_size, max_size)
        except ValueError:
            print("Invalid size range format.")
            return
    
    results = search_files(file_index, name, file_type, mod_date, size, date_range, size_range, match_case, match_whole_word, match_diacritics)
    
    if results:
        print("\nSearch Results:")
        for res in results:
            print(json.dumps(res, indent=4))
    else:
        print("No matching files found.")

if __name__ == "__main__":
    main()
