import os
import json
import time

def index_files(directory, output_json):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    indexed_data = []
    
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            mod_time = time.ctime(os.path.getmtime(dir_path))
            indexed_data.append({
                "Name": dir_name,
                "Path": dir_path,
                "Type": "Directory",
                "Modification Time": mod_time,
                "Size (bytes)": "N/A"
            })  # No size for directories
        
        for file in files:
            file_path = os.path.join(root, file)
            file_type = os.path.splitext(file)[1]
            mod_time = time.ctime(os.path.getmtime(file_path))
            file_size = os.path.getsize(file_path)  # Get file size
            indexed_data.append({
                "Name": file,
                "Path": file_path,
                "Type": file_type,
                "Modification Time": mod_time,
                "Size (bytes)": file_size
            })

    os.makedirs(os.path.dirname(output_json), exist_ok=True)  # Ensure output directory exists
    with open(output_json, mode='w', encoding='utf-8') as json_file:
        json.dump(indexed_data, json_file, indent=4)
    
    print(f"\nIndexing complete. Data saved to {output_json}")

if __name__ == "__main__":
    directory_to_scan = os.path.abspath("C://Users//nachi//Documents//smart search//test")
    output_file = os.path.abspath("../Indexrecord/file_index.json")
    
    index_files(directory_to_scan, output_file)
