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
DB_NAME = "file_monitor"

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
               match_case_exclude=False, match_whole_word_exclude=False, match_diacritics_exclude=False):
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
        if min_size and max_size:
            conditions.append("size BETWEEN %s AND %s")
            values.extend([min_size, max_size])
        elif min_size:
            conditions.append("size >= %s")
            values.append(min_size)
        elif max_size:
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
        results = [list(row) for row in cursor.fetchall()]  # Convert tuples to lists

        # Close resources
        cursor.close()
        conn.close()

        return results  

    except mysql.connector.Error as e:
        logging.error("Database error occurred", exc_info=True)
        return []

# User input with defaults
if __name__ == "__main__":
    name_pattern = input("Enter name pattern (leave blank to ignore): ") or None
    file_type = input("Enter file type (leave blank to ignore): ") or None
    start_date = validate_date(input("Enter start date (YYYY-MM-DD, leave blank to ignore): "))
    end_date = validate_date(input("Enter end date (YYYY-MM-DD, leave blank to ignore): "))
    
    min_size = input("Enter minimum file size (bytes, leave blank to ignore): ")
    max_size = input("Enter maximum file size (bytes, leave blank to ignore): ")

    # Convert size inputs to integers if provided
    min_size = int(min_size) if min_size else None
    max_size = int(max_size) if max_size else None

    # Filename match options
    match_case = input("Match case for filename? (yes/no): ").strip().lower() == 'yes'
    match_whole_word = input("Match whole word for filename? (yes/no): ").strip().lower() == 'yes'
    match_diacritics = input("Match diacritics for filename? (yes/no): ").strip().lower() == 'yes'

    # Exclude words input
    exclude_words_input = input("Enter words to exclude (comma-separated, leave blank to ignore): ")
    exclude_words = [word.strip() for word in exclude_words_input.split(',')] if exclude_words_input else None

    # Exclude words match options
    match_case_exclude = input("Match case for excluding words? (yes/no): ").strip().lower() == 'yes'
    match_whole_word_exclude = input("Match whole word for excluding words? (yes/no): ").strip().lower() == 'yes'
    match_diacritics_exclude = input("Match diacritics for excluding words? (yes/no): ").strip().lower() == 'yes'

    # Fetch and display results
    results = fetch_data(name_pattern, file_type, start_date, end_date, min_size, max_size, 
                         match_case, match_whole_word, match_diacritics, 
                         exclude_words, match_case_exclude, match_whole_word_exclude, match_diacritics_exclude)

    # Output results as list of lists
    print("\nResults (List of Lists):")
    print(results)
