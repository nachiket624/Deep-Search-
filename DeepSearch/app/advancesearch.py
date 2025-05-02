import mysql.connector
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Database credentials
DB_HOST = "localhost"
DB_USER = os.getenv("DB_USER", "root")  
DB_PASSWORD = os.getenv("DB_PASSWORD", "1900340220")  # Replace with a secure method
DB_NAME = "dbdeepsearch"

def validate_date(date_str):
    """Validates and converts a date string to a date object."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.")
        return None

def fetch_data(name_pattern=None, file_type=None, start_date=None, end_date=None, 
               min_size=None, max_size=None, match_case=False, match_whole_word=False, 
               match_diacritics=False, exclude_words=None, 
               match_case_exclude=False, match_whole_word_exclude=False, match_diacritics_exclude=False,
               folder_path=None):
    try:
        # Establish the connection
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Base query and values list
        conditions = ["1=1"]  
        values = []

        # Handle folder path filtering
        if folder_path:
            print(folder_path)
            normalized_path = folder_path.replace("/", "\\").lower().strip("\\")
            parts = [part for part in normalized_path.split("\\") if part]
            if parts:
                like_pattern = parts[0] + "%" + "%".join(parts[1:]) + "%"
                conditions.append("LOWER(path) LIKE %s")
                values.append(like_pattern)

        # Handle name pattern matching
        if name_pattern:
            collation = "BINARY" if match_case or match_diacritics else "utf8mb4_general_ci"
            if match_whole_word:
                conditions.append(f"name = %s COLLATE {collation}")
                values.append(name_pattern)
            else:
                conditions.append(f"name LIKE %s COLLATE {collation}")
                values.append(f"%{name_pattern}%")

        # Filter by file type
        if file_type:
            conditions.append("type = %s")
            values.append(file_type)

        # Filter by modification date
        if start_date and end_date:
            conditions.append("modification_time BETWEEN %s AND %s")
            values.extend([start_date, end_date])
        elif start_date:
            conditions.append("modification_time >= %s")
            values.append(start_date)
        elif end_date:
            conditions.append("modification_time <= %s")
            values.append(end_date)

        # Filter by file size
        if min_size is not None and max_size is not None:
            conditions.append("size BETWEEN %s AND %s")
            values.extend([min_size, max_size])
        elif min_size is not None:
            conditions.append("size >= %s")
            values.append(min_size)
        elif max_size is not None:
            conditions.append("size <= %s")
            values.append(max_size)

        # Exclude words from filename
        if exclude_words:
            for word in exclude_words:
                collation_exclude = "BINARY" if match_case_exclude or match_diacritics_exclude else "utf8mb4_general_ci"
                if match_whole_word_exclude:
                    conditions.append(f"name != %s COLLATE {collation_exclude}")
                    values.append(word)
                else:
                    conditions.append(f"name NOT LIKE %s COLLATE {collation_exclude}")
                    values.append(f"%{word}%")

        # Construct the final SQL query
        query = "SELECT id, name, path, type, modification_time, size FROM files WHERE " + " AND ".join(conditions)

        # Execute query
        cursor.execute(query, values)
        print(format_query(query,values))
        results = [list(row) for row in cursor.fetchall()]  # Convert tuples to lists

        # Close resources
        cursor.close()
        conn.close()

        return results  

    except mysql.connector.Error as e:
        logging.error("Database error occurred", exc_info=True)
        return []


def format_query(query, values):
    def format_value(v):
        if isinstance(v, str):
            return f"'{v}'"
        elif v is None:
            return 'NULL'
        else:
            return str(v)
    
    parts = query.split('%s')
    full_query = ''
    for part, val in zip(parts, values + ['']):
        full_query += part + format_value(val)
    return full_query

