import json
import os
from datetime import datetime

# File type extension groups
MUSIC_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac"}
DOC_EXTENSIONS = {".doc", ".docx", ".pdf", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".rtf"}
PICTURE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".mpeg"}
EXECUTABLE_EXTENSIONS = {".exe", ".bat", ".sh", ".app", ".msi"}
COMPRESSED_EXTENSIONS = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"}

def load_index(file_path):
    """Load file index from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: file_index.json not found.")
    except json.JSONDecodeError:
        print("Error: JSON file is corrupted or incorrectly formatted.")
    return []

def search_files(index, name=None, file_type=None, mod_date=None, size=None):
    """Search for files and folders based on given criteria."""
    results = []
    
    for entry in index:
        file_name = entry["Name"].lower()
        entry_type = entry.get("Type", "file").lower()  # Default type is file if not specified

        if name and name.lower() not in file_name:
            continue
        
        # Handle special file types and folders
        if file_type:
            if file_type.lower() == "music":
                if not any(file_name.endswith(ext) for ext in MUSIC_EXTENSIONS):
                    continue
            elif file_type.lower() == "doc":
                if not any(file_name.endswith(ext) for ext in DOC_EXTENSIONS):
                    continue
            elif file_type.lower() == "picture":
                if not any(file_name.endswith(ext) for ext in PICTURE_EXTENSIONS):
                    continue
            elif file_type.lower() == "video":
                if not any(file_name.endswith(ext) for ext in VIDEO_EXTENSIONS):
                    continue
            elif file_type.lower() == "exe":
                if not any(file_name.endswith(ext) for ext in EXECUTABLE_EXTENSIONS):
                    continue
            elif file_type.lower() == "compressed":
                if not any(file_name.endswith(ext) for ext in COMPRESSED_EXTENSIONS):
                    continue
            elif file_type.lower() == "folder":
                if entry_type != "folder":
                    continue
            elif not file_name.endswith(file_type.lower()):
                continue
        
        if mod_date:
            try:
                entry_mod_time = datetime.strptime(entry["Modification Time"], "%a %b %d %H:%M:%S %Y")
                if datetime.strptime(mod_date, "%Y-%m-%d").date() != entry_mod_time.date():
                    continue
            except ValueError:
                print(f"Warning: Invalid date format in index for {entry['Name']}")
                continue
        
        if size and entry["Size (bytes)"].isdigit():
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
    
    print("Search files by name, type (e.g., .txt, .pdf, music, doc, picture, video, exe, compressed, folder), modification date (YYYY-MM-DD), or size.")
    name = input("Enter file/folder name (or part of it, leave blank to skip): ").strip()
    file_type = input("Enter file extension (e.g., .txt, .pdf) or type 'music', 'doc', 'picture', 'video', 'exe', 'compressed', 'folder' (leave blank to skip): ").strip()
    mod_date = input("Enter modification date (YYYY-MM-DD, leave blank to skip): ").strip()
    size_input = input("Enter file size in bytes (leave blank to skip): ").strip()
    
    size = int(size_input) if size_input.isdigit() else None

    try:
        if mod_date:
            datetime.strptime(mod_date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    results = search_files(file_index, name, file_type, mod_date, size)
    
    if results:
        print("\nSearch Results:")
        for res in results:
            print(json.dumps(res, indent=4))
    else:
        print("No matching files or folders found.")

if __name__ == "__main__":
    main()
