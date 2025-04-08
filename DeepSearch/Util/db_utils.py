import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

ALLOWED_EXTENSIONS = {
    ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac",
    ".doc", ".docx", ".pdf", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".rtf",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp",
    ".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".mpeg",
    ".exe", ".bat", ".sh", ".app", ".msi",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"
}

DB_CONFIG = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database":DB_NAME
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        path VARCHAR(512) UNIQUE,
                        type VARCHAR(50),
                        modification_time DATETIME,
                        size BIGINT)''')
    conn.commit()
    conn.close()

def formatdate(filedatetime):
    return datetime.fromtimestamp(filedatetime).strftime('%Y-%m-%d %H:%M:%S')
