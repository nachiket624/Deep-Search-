import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import os
from pathlib import Path
from cryptography.fernet import Fernet
from getpass import getpass
import logging
import json

CONFIG_FILE = "config.json"
KEY_FILE = "secret.key"
MAX_LOG_SIZE_MB = 20
LOG_FILE = "deepsearchapp.log"
DB_HOST = "localhost"
DB_NAME = "dbdeepsearch"


ALLOWED_EXTENSIONS = {
    "",
    ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac",
    ".doc", ".docx", ".pdf", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".rtf",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp",
    ".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".mpeg",
    ".exe", ".bat", ".sh", ".app", ".msi",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"
}

MAX_LOG_SIZE_MB = 5

# Use user-writable location
LOG_DIR = os.path.join(os.getenv('APPDATA'), 'NexaTech', 'Deep Search')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, 'deepsearchapp.log')

# Remove log if too large
if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE_MB * 1024 * 1024:
    os.remove(LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Encryption / Credential Handling ---
def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def encrypt(text, fernet):
    return fernet.encrypt(text.encode()).decode()

def decrypt(token, fernet):
    return fernet.decrypt(token.encode()).decode()


def load_credentials():
    key = load_or_create_key()
    fernet = Fernet(key)
    
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    try:
        username = decrypt(data["username"], fernet)
        password = decrypt(data["password"], fernet)
        return username, password
    except Exception:
        logging.error("Failed to decrypt credentials. Re-entering...")

    


def get_db_connection(use_database=True):
    try:
        username, password = load_credentials()
        config = {
            "host": DB_HOST,
            "user": username,
            "password": password,
        }
        if use_database:
            config["database"] = DB_NAME
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        logging.error(f"DB Connection Error: {err}")
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


# get_db_connection()