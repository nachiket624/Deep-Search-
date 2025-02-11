import os
import json
import time
from tqdm import tqdm

def index_files(directory, output_json):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    all_items = []
    
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            mod_time = time.ctime(os.path.getmtime(dir_path))
            all_items.append((dir_path, "Directory", mod_time, None))  # No size for directories
        
        for file in files:
            file_path = os.path.join(root, file)
            file_type = os.path.splitext(file)[1]
            mod_time = time.ctime(os.path.getmtime(file_path))
            file_size = os.path.getsize(file_path)  # Get file size
            all_items.append((file_path, file_type, mod_time, file_size))

    indexed_data = []
    for path, item_type, mod_time, size in tqdm(all_items, desc="Indexing items", unit="item"):
        entry = {
            "Path": path,
            "Type": item_type,
            "Modification Time": mod_time,
            "Size (bytes)": size if size is not None else "N/A"
        }
        indexed_data.append(entry)
    
    os.makedirs(os.path.dirname(output_json), exist_ok=True)  # Ensure output directory exists
    with open(output_json, mode='w', encoding='utf-8') as json_file:
        json.dump(indexed_data, json_file, indent=4)
    
    print(f"\nIndexing complete. Data saved to {output_json}")

if __name__ == "__main__":
    directory_to_scan = os.path.abspath("C://Users//nachi//Documents//Projects")
    output_file = os.path.abspath("../Indexrecord/file_index.json")
    
    index_files(directory_to_scan, output_file)
