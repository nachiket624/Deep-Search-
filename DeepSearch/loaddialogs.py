from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from Mainwindow.Dialogs import advsearch, textresult
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt
import qtawesome as qta
from Modules.Search.searchtxt import search_files

class LoadTextResult(QtWidgets.QDialog, textresult.Ui_Dialog):
    def __init__(self, phrase=""):
        super().__init__()
        self.setupUi(self)
        self.display_search_phrase(phrase)

    def display_search_phrase(self, phrase):
        data = search_files(phrase)
        self.tableWidget.setRowCount(len(data)+1)  # Set rows
        self.tableWidget.setColumnCount(3)  # 3 Columns for title, path, and content preview
        self.tableWidget.setHorizontalHeaderLabels(["Title", "Path", "Content Preview"])
        
        column_widths = [100,500,1000]  # Widths for each column
        for col, width in enumerate(column_widths):
            self.tableWidget.setColumnWidth(col, width)

    # Populate Table
        for row, item in enumerate(data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(item[0])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(item[1]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(item[2]))
            

class LoadAdvSearch(QtWidgets.QDialog, advsearch.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.w = None
        self.setupUi(self)
        # Set icons
        browsefile_icon = qta.icon('ph.folder-notch-open-fill', color="yellow")
        self.digadvborwesfile.setIcon(browsefile_icon)

        search_icon = qta.icon('fa5s.search', color='green')
        self.digadvsearchbtn.setIcon(search_icon)

        cancel_icon = qta.icon('mdi.cancel', color='red')
        self.digadvcancelbtn.setIcon(cancel_icon)

        # Connect search button to function
        self.digadvsearchbtn.clicked.connect(self.search)

    def search(self):
        phrase_input = self.phraseinput.text().strip()
        
        if not phrase_input:
            QMessageBox.warning(self, "Input Error", "Please enter a search phrase.")
            return

        if self.w is None or not self.w.isVisible():
            self.w = LoadTextResult(phrase_input)  # Pass phrase to LoadTextResult
        else:
            self.w.display_search_phrase(phrase_input)  # Update if already open

        self.w.show()
