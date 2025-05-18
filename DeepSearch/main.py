from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal
from PySide6.QtWidgets import *
import sys
import os
import json
from getpass import getpass
from cryptography.fernet import Fernet
# from qt_material import apply_stylesheet
import qdarktheme
import qtawesome as qta
from app.MainWindow import Ui_MainWindow
import app.loaddialogs as loaddialogs
from dbconnection.db_utils import ALLOWED_EXTENSIONS,get_db_connection

EXTENSION_GROUPS = ALLOWED_EXTENSIONS
HOME_DIR = os.path.expanduser("~")
CONFIG_FILE = os.path.join(HOME_DIR, ".myapp_config.json")
KEY_FILE = os.path.join(HOME_DIR, ".myapp_key.key")
MAX_LOG_SIZE_MB = 20
LOG_FILE = "deepsearchapp.log"
DB_HOST = "localhost"
DB_NAME = "dbdeepsearch"

basedir = os.path.dirname(__file__)
try:
    from ctypes import windll  
    myappid = 'Nexatech.DeepSearch.1.0.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


def get_enabled_actions(actions):
    return [action for action in actions if action.isChecked()]

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
    
def search_files_in_db(filename, filetypes=None):
    conn = get_db_connection()
    if filetypes: 
        typelist = {ext for ft in filetypes if ft in EXTENSION_GROUPS for ext in EXTENSION_GROUPS[ft]}
    else: 
        typelist = set()
    type_conditions = ', '.join(f"'{ext}'" for ext in typelist)

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
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.w = None
        self.w1 = None
        self.setupUi(self)
        self.setWindowTitle("Deep Search")
        self.setWindowIcon(QIcon('./assets/icon.png'))
        QtCore.QTimer.singleShot(0, self.post_ui_load)
        adjicon = qta.icon('ei.adjust-alt')
        self.advsearchbtn.setIcon(adjicon)
        self.advsearchbtn.clicked.connect(self.showadvsearchdig)
        self.lineeditsearch.returnPressed.connect(self.Search)
        self.actionSettings.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        browsefile_icon = qta.icon('ph.folder-notch-open-fill', color="yellow")
        self.openindexdir.setIcon(browsefile_icon)
        self.cancelBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.openindexdir.clicked.connect(self.select_folder)
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
    
    def post_ui_load(self):
        self.load_credentials()
        self.data = fetch_all_files()  
        self.tableWidget.setRowCount(len(self.data)) 
        self.tablestyle()
        self.update_table()
       
    
    def load_or_create_key(self):
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "rb") as f:
                return f.read()
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

    def encrypt(self, text, fernet):
        return fernet.encrypt(text.encode()).decode()

    def decrypt(self, token, fernet):
        return fernet.decrypt(token.encode()).decode()

    def loginwindow(self):
        self.stackedWidget.setCurrentIndex(1)
        key = self.load_or_create_key()
        fernet = Fernet(key)
        self.btndbconnct.clicked.connect(lambda: self.save_credentials(fernet))

    def save_credentials(self, fernet):
        username = self.dbusername.text()
        password = self.dbpass.text()
        if not username or not password:
            return
        data = {
            "username": self.encrypt(username, fernet),
            "password": self.encrypt(password, fernet)
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)
        os.chmod(CONFIG_FILE, 0o600)

    def load_credentials(self):
        key = self.load_or_create_key()
        fernet = Fernet(key)

        if not os.path.exists(CONFIG_FILE):
            self.loginwindow()
            return None  # Wait for user to click save

        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
            username = self.decrypt(data["username"], fernet)
            password = self.decrypt(data["password"], fernet)
            return username, password

        except Exception as e:
            os.remove(CONFIG_FILE)
            self.loginwindow()
            return None  # Wait for user to click save
        

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.pathindexdir.setText(folder_path)
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

        filename = self.lineeditsearch.text().strip()
        if not filename:
            QMessageBox.warning(self, "Input Error", "Please enter a file name to search.")
            return
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
    window.show()
    app.exec()
