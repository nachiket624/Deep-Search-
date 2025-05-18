import mysql.connector
import os
import logging
from datetime import datetime
from dbconnection.db_utils import ALLOWED_EXTENSIONS,get_db_connection

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

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
               min_size=None, max_size=None,allthisword =None ,match_case=False, match_whole_word=False, 
               match_diacritics=False, exclude_words=None, 
               match_case_exclude=False, match_whole_word_exclude=False, match_diacritics_exclude=False,
               folder_path=None):
    try:
        # Establish the connection
        conn = get_db_connection()
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

        if allthisword:
            if match_case or match_diacritics:
                collation = "utf8mb4_bin"  # Case & diacritic sensitive
            else:
                collation = "utf8mb4_general_ci"  # Case & diacritic insensitive

            if match_whole_word:
                # Exact word match
                conditions.append(f"name COLLATE {collation} = %s")
                values.append(allthisword)
            else:
                # Partial word match
                conditions.append(f"name COLLATE {collation} LIKE %s")
                values.append(f"%{allthisword}%")

                
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
                if match_case_exclude or match_diacritics_exclude:
                    collation_exclude = "utf8mb4_bin"  # Case & diacritic sensitive
                else:
                    collation_exclude = "utf8mb4_general_ci"  # Insensitive

                if match_whole_word_exclude:
                    conditions.append(f"name COLLATE {collation_exclude} != %s")
                    values.append(word)
                else:
                    conditions.append(f"name COLLATE {collation_exclude} NOT LIKE %s")
                    values.append(f"%{word}%")

        query = "SELECT id, name, path, type, modification_time, size FROM files WHERE " + " AND ".join(conditions)
        cursor.execute(query, values)
        results = [list(row) for row in cursor.fetchall()]  # Convert tuples to lists

        # Close resources
        cursor.close()
        conn.close()

        return results  

    except mysql.connector.Error as e:
        logging.error("Database error occurred", exc_info=True)
        return []
