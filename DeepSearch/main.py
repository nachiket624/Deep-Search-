from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtWidgets import *
import sys
# from qt_material import apply_stylesheet
import qdarktheme
import qtawesome as qta
from search.simplesearch import search_files_db
from app.MainWindow import Ui_MainWindow
import app.loaddialogs as loaddialogs
from dbconnection.db_utils import create_database_if_not_exists,create_table,ALLOWED_EXTENSIONS,get_db_connection

EXTENSION_GROUPS = ALLOWED_EXTENSIONS

def fetch_all_files():
    """Fetch all file records from the MySQL database."""
    conn = get_db_connection(use_database=True)
    if conn is None:
        return
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, path, type, modification_time, size FROM files LIMIT 100")
    data = cursor.fetchall()
    conn.close()
    return data
    return []

def search_files_in_db(filename, filetypes=None):
    conn = get_db_connection()
    if filetypes: 
        typelist = {ext for ft in filetypes if ft in EXTENSION_GROUPS for ext in EXTENSION_GROUPS[ft]}
    else: 
        typelist = set()
    type_conditions = ', '.join(f"'{ext}'" for ext in typelist)

    print("Type Condition:", type_conditions)

    if conn:
        cursor = conn.cursor(dictionary=True)
        if typelist: 
            query = f"""
                SELECT name, path, type, modification_time, size 
                FROM files 
                WHERE name LIKE %s AND type IN ({type_conditions})
            """
            cursor.execute(query, (f"%{filename}%",))
        else:
            query = "SELECT name, path, type, modification_time, size FROM files WHERE name LIKE %s"
            cursor.execute(query, (f"%{filename}%",))
        results = cursor.fetchall()
        conn.close()
        return results
    return []


def get_enabled_actions(actions):
    return [action for action in actions if action.isChecked()]

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.w = None
        self.w1 = None
        self.setupUi(self)
        self.setWindowTitle("Deep Search")
        self.data = fetch_all_files()  # Fetch data from MySQL
        self.tableWidget.setRowCount(len(self.data))  # Set row count
        self.tablestyle()
        self.update_table()
        adjicon = qta.icon('ei.adjust-alt')
        self.advsearchbtn.setIcon(adjicon)
        self.advsearchbtn.clicked.connect(self.showadvsearchdig)
        self.lineeditsearch.returnPressed.connect(self.Search)
        self.music = self.actionAudio
        self.doc = self.actionDocument
        self.picture = self.actionPicture
        self.video = self.actionVideo
        self.folder = self.actionFolder
        self.exe = self.actionExecutable
        self.compressed = self.actionCompressed
        self.music.triggered.connect(self.Search)
        self.doc.triggered.connect(self.Search)
        self.picture.triggered.connect(self.Search)
        self.video.triggered.connect(self.Search)
        self.folder.triggered.connect(self.Search)
        self.exe.triggered.connect(self.Search)
        self.compressed.triggered.connect(self.Search)


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
        actions = [self.music,self.doc,self.picture,self.video,self.exe,self.compressed]
        enabled_actions = get_enabled_actions(actions)
        filetype = ([action.text() for action in enabled_actions])
        print(filetype)

        filename = self.lineeditsearch.text().strip()
        if not filename:
            QMessageBox.warning(self, "Input Error", "Please enter a file name to search.")
            return

        print(f"Searching for: {filename}")
        results = search_files_in_db(filename,filetype)
        if results:
            self.data = results
            self.update_table()
        else:
            QMessageBox.information(self, "No Results", "No matching files found.")

    def showadvsearchdig(self, checked):
        """Show advanced search dialog."""
        if self.w is None:
            self.w = loaddialogs.LoadAdvSearch(self)  # Pass main window reference
            self.w.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Ensures proper cleanup
            self.w.show()
            self.w.destroyed.connect(self.clear_dialog_reference)  # Reset reference when closed
        else:
            self.w.raise_()  # Bring the window to the front
            self.w.activateWindow()  # Focus the window

    def clear_dialog_reference(self):
        """Clear dialog reference when it is closed."""
        self.w = None
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # apply_stylesheet(app, theme='dark_purple.xml')
    qdarktheme.setup_theme()
    window = MainWindow()
    create_database_if_not_exists()
    create_table()
    window.show()
    app.exec()
