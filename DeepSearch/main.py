from PySide6 import QtWidgets
from PySide6.QtWidgets import *
import sys
import mysql.connector
from qt_material import apply_stylesheet
import qtawesome as qta

# UI element
from Mainwindow.MainWindow import Ui_MainWindow
import loaddialogs

# MySQL Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "1900340220"
DB_NAME = "file_monitor"

def connect_db():
    """Establish a database connection."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def fetch_all_files():
    """Fetch all file records from the MySQL database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, path, type, modification_time, size FROM files")
        data = cursor.fetchall()
        conn.close()
        return data
    return []

def search_files_in_db(filename):
    """Search files in the MySQL database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT name, path, type, modification_time, size FROM files WHERE name LIKE %s"
        cursor.execute(query, (f"%{filename}%",))
        results = cursor.fetchall()
        conn.close()
        return results
    return []

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.w = None
        self.w1 = None
        self.setupUi(self)
        
        self.data = fetch_all_files()  # Fetch data from MySQL
        self.tableWidget.setRowCount(len(self.data))  # Set row count
        
        self.tablestyle()
        self.update_table()

        adjicon = qta.icon('ei.adjust-alt')
        self.advsearchbtn.setIcon(adjicon)
        self.advsearchbtn.clicked.connect(self.showadvsearchdig)
        self.lineeditsearch.returnPressed.connect(self.Search)

    def tablestyle(self):
        """Set table styles and column widths."""
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        table_header = ["Name", "Path", "Type", "Modification Time", "Size (bytes)"]
        self.tableWidget.setHorizontalHeaderLabels(table_header)
        column_widths = [300, 600, 100, 300, 140]
        for col, width in enumerate(column_widths):
            self.tableWidget.setColumnWidth(col, width)

    def update_table(self):
        """Update table with data from MySQL."""
        if not self.data:
            return

        self.tableWidget.setRowCount(len(self.data))
        for row, entry in enumerate(self.data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(entry.get("name", "N/A")))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(entry.get("path", "N/A")))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(entry.get("type", "N/A")))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(entry.get("modification_time", "N/A"))))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(entry.get("size", "N/A"))))

    def Search(self):
        """Perform search in the MySQL database."""
        filename = self.lineeditsearch.text().strip()
        if not filename:
            QMessageBox.warning(self, "Input Error", "Please enter a file name to search.")
            return

        print(f"Searching for: {filename}")
        results = search_files_in_db(filename)
        if results:
            self.data = results
            self.update_table()
        else:
            QMessageBox.information(self, "No Results", "No matching files found.")

    def showadvsearchdig(self, checked):
        """Show advanced search dialog."""
        if self.w is None:
            self.w = loaddialogs.LoadAdvSearch()
        self.w.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_purple.xml')
    window = MainWindow()
    window.show()
    app.exec()
