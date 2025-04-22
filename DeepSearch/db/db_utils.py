import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "dbdeepsearch"

ALLOWED_EXTENSIONS = {
    ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac",
    ".doc", ".docx", ".pdf", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".rtf",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp",
    ".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".mpeg",
    ".exe", ".bat", ".sh", ".app", ".msi",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"
}

def get_db_connection(use_database=True):
    try:
        config = {
            "host": DB_HOST,
            "user": DB_USER,
            "password": DB_PASSWORD,
        }
        if use_database:
            config["database"] = DB_NAME
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(f"DB Connection Error: {err}")
        return None

def create_database_if_not_exists():
    conn = get_db_connection(use_database=False)
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    conn.close()

def create_table():
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        path VARCHAR(512) UNIQUE,
                        type VARCHAR(50),
                        modification_time DATETIME,
                        size BIGINT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                     )''')
    conn.commit()
    conn.close()

def formatdate(filedatetime):
    return datetime.fromtimestamp(filedatetime).strftime('%Y-%m-%d %H:%M:%S')

