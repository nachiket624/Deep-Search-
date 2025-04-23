from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from app import advsearch, textresult
from PySide6.QtWidgets import QTableWidgetItem
import qtawesome as qta
from PySide6.QtCore import Qt
from dotenv import load_dotenv
import os
from search import searchtxt,searchdocx,searchpdf
from app import advancesearch 
import subprocess
import platform

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

EXTENSION_GROUPS =["",".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".alac",".doc", ".docx", ".pdf",
                    ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".rtf",".jpg", ".jpeg", ".png", 
                    ".gif", ".bmp", ".tiff", ".svg", ".webp",".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".mpeg"
                    ".exe", ".bat", ".sh", ".app", ".msi",".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"]


class LoadTextResult(QtWidgets.QDialog, textresult.Ui_Dialog):
    def __init__(self, phrase=""):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinMaxButtonsHint |
            Qt.WindowCloseButtonHint
        )
        self.setWindowTitle("Text Matech") 
        self.tableWidget.cellClicked.connect(self.open_path_in_explorer)
        self.display_search_phrase(phrase)

    def display_search_phrase(self, phrase):
        docdata = searchdocx.search_files(phrase)
        pdfdata = searchpdf.search_files(phrase)
        txtdata = searchtxt.search_files(phrase)
        data = docdata + pdfdata + txtdata
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(3)  
        self.tableWidget.setHorizontalHeaderLabels(["Title", "Path", "Content Preview"])
        
        column_widths = [100,500,1000] 
        for col, width in enumerate(column_widths):
            self.tableWidget.setColumnWidth(col, width)

        for row, item in enumerate(data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(item[0])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(item[1]))
            preview_item = QTableWidgetItem(item[2])
            preview_item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
            preview_item.setFlags(preview_item.flags() ^ Qt.ItemIsEditable)
            self.tableWidget.setItem(row, 2, preview_item)
        self.tableWidget.resizeRowsToContents()
    def open_path_in_explorer(self, row, column):
        if column == 1:  # Path column
            item = self.tableWidget.item(row, column)
            if item:
                path = item.text()
                if os.path.exists(path):
                    if platform.system() == "Windows":
                        os.startfile(path)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", path])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", path])
                else:
                    QtWidgets.QMessageBox.warning(self, "Path Not Found", f"The path does not exist:\n{path}")

class LoadAdvSearchResult(QtWidgets.QDialog, textresult.Ui_Dialog):
    def __init__(self,data):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinMaxButtonsHint |
            Qt.WindowCloseButtonHint
        )
        self.setWindowTitle("Advance File Search")
        self.tableWidget.cellClicked.connect(self.open_path_in_explorer)
        self.tablestyle()
        self.update_table(data)
    def tablestyle(self):
        """Set table styles and column widths."""
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget.setColumnCount(5)  
        table_header = ["Name", "Path", "Type", "Modification Time", "Size (bytes)"]
        self.tableWidget.setHorizontalHeaderLabels(table_header)
        column_widths = [300, 600, 100, 300, 140]
        for col, width in enumerate(column_widths):
            self.tableWidget.setColumnWidth(col, width)
    def update_table(self,data):
        """Update table with data from MySQL."""
        if not data:
            return
        self.tableWidget.setRowCount(len(data))
        for row, entry in enumerate(data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(entry[1]))  # Name
            self.tableWidget.setItem(row, 1, QTableWidgetItem(entry[2]))  # Path
            self.tableWidget.setItem(row, 2, QTableWidgetItem(entry[3]))  # Type
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(entry[4])))  # Modification Time
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(entry[5])))  # Size
    def open_path_in_explorer(self, row, column):
        if column == 1:  # Path column
            item = self.tableWidget.item(row, column)
            if item:
                path = item.text()
                if os.path.exists(path):
                    if platform.system() == "Windows":
                        os.startfile(path)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", path])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", path])
                else:
                    QtWidgets.QMessageBox.warning(self, "Path Not Found", f"The path does not exist:\n{path}")

class LoadAdvSearch(QtWidgets.QDialog, advsearch.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.showresult = textresult.Ui_Dialog
        self.w = None
        self.setupUi(self)
        self.setWindowTitle("Adavance Search")
        browsefile_icon = qta.icon('ph.folder-notch-open-fill', color="yellow")
        self.digadvborwesfile.setIcon(browsefile_icon)
        search_icon = qta.icon('fa5s.search', color='green')
        self.digadvsearchbtn.setIcon(search_icon)
        self.serchphrasebtn.setIcon(search_icon)
        self.serchphrasebtn.clicked.connect(self.TextSearch)
        cancel_icon = qta.icon('mdi.cancel', color='red')
        self.digadvcancelbtn.setIcon(cancel_icon)
        self.phraseinput.textEdited.connect(self.checkserchcondition)
        if self.filenameinput.textChanged:
            self.phraseinput.setDisabled(False)
            self.serchphrasebtn.setDisabled(False)
        self.digadvcancelbtn.clicked.connect(self.closeadvsearch)  
        self.digadvsearchbtn.clicked.connect(self.filesearch)
        self.fileextationinput.addItems(EXTENSION_GROUPS)
       
    def filesearch(self):
        name_pattern = self.filenameinput.text()
        file_type = self.fileextationinput.currentText()
        start_date = self.startdate.text()
        end_date = self.enddate.text()
        min_size = self.fileminsize.text()
        max_size = self.filemaxsize.text()
        match_case = self.filemachcase.isChecked()
        match_whole_word = self.filematchwholeword.isChecked()
        match_diacritics = self.filematchdiacribcs.isChecked()
        exclude_words = self.excludewords.text()
        match_case_exclude = self.fileexactphrasematchcase.isChecked()
        match_whole_word_exclude = self.fileexactmactchwholeword.isChecked()
        match_diacritics_exclude = self.fileexactmatchdiacribcs.isChecked()

        advdata = advancesearch.fetch_data(name_pattern,file_type,start_date,end_date,min_size,max_size,match_case,match_whole_word,match_diacritics,exclude_words,match_case_exclude,match_whole_word_exclude,match_diacritics_exclude)
        if self.w is None or not self.w.isVisible():
            self.w = LoadAdvSearchResult(advdata) 
        else:
            self.w.update_table(advdata) 
        self.w.exec()
    
    def checkserchcondition(self):
        self.digadvsearchbtn.setDisabled(True)
        if len(self.phraseinput.text())<=0:
            self.digadvsearchbtn.setDisabled(False)
    def closeadvsearch(self):
        self.close()
              
    def TextSearch(self):
        phrase_input = self.phraseinput.text().strip()
        
        if not phrase_input:
            QMessageBox.warning(self, "Input Error", "Please enter a search phrase.")
            return

        if self.w is None or not self.w.isVisible():
            self.w = LoadTextResult(phrase_input) 
        else:
            self.w.display_search_phrase(phrase_input) 
        self.w.exec()