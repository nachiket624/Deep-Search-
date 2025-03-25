import mysql.connector
import logging
import logging
# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

# File type extension groups
EXTENSION_GROUPS = {
    "music": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac"},
    "doc": {".doc", ".docx", ".pdf", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".rtf"},
    "picture": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"},
    "video": {".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".mpeg"},
    "exe": {".exe", ".bat", ".sh", ".app", ".msi"},
    "compressed": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"},
}

# Database Configuration (Update with your MySQL credentials)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1900340220",
    "database": "file_monitor"
}

def load_index():
    """Load file index from MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, path, type, modification_time, size FROM files")
        records = cursor.fetchall()

        cursor.close()
        conn.close()
        return records

    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        return []



def search_files_db(name=None, file_types=None):
    """Search files using SQL query for efficiency. Returns results as a list of lists."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "SELECT id, name, path, type, modification_time, size FROM files WHERE 1=1"
        params = []

        if name:
            query += " AND name LIKE %s"
            params.append(f"%{name}%")

        if file_types:
            if isinstance(file_types, list):  # Handling multiple file extensions
                query += " AND (" + " OR ".join(["name LIKE %s" for _ in file_types]) + ")"
                params.extend([f"%.{ext}" for ext in file_types])
            elif file_types in EXTENSION_GROUPS:  # Handling predefined extension groups
                query += " AND (" + " OR ".join(["name LIKE %s" for ext in EXTENSION_GROUPS[file_types]]) + ")"
                params.extend([f"%.{ext}" for ext in EXTENSION_GROUPS[file_types]])
            elif file_types == "folder":
                query += " AND type = 'folder'"
            else:
                query += " AND name LIKE %s"
                params.append(f"%.{file_types}")

        cursor.execute(query, params)
        results = cursor.fetchall()  # Returns list of tuples

        cursor.close()
        conn.close()

        return [list(row) for row in results]  # Convert tuples to lists

    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        return []




def main():
   
    
    print("Search files by name, type, modification date, or size.")
    name = input("Enter file/folder name (or part of it, leave blank to skip): ").strip()
    file_type = input("Enter file extension (e.g., .txt, .pdf) or type 'music', 'doc', 'picture', 'video', 'exe', 'compressed', 'folder' (leave blank to skip): ").strip().lower()
    

    results = search_files_db(name, file_type)
    
    if results:
        print("\nSearch Results:")
        for res in results:
            print(f"📄 Name: {res['name']}\n📂 Path: {res['path']}\n🗂 Type: {res['type']}\n🕒 Modified: {res['modification_time']}\n📏 Size: {res['size']} bytes\n{'-'*40}")
    else:
        print("No matching files or folders found.")

if __name__ == "__main__":
    main()
