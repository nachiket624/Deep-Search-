from PySide6 import QtWidgets
from PySide6.QtWidgets import *
import sys
import json
from qt_material import apply_stylesheet
import qtawesome as qta

# ui element
from Mainwindow.MainWindow import Ui_MainWindow
import loaddialogs
from Modules.Search.searchtxt import serach_text


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.w = None
        self.w1 = None
        self.setupUi(self)
        self.tablestyle()
        json_file = "../DeepSearch/Modules/Indexrecord/file_index.json"  # Ensure this file exists
        self.data = self.load_json(json_file)  # Store data in an instance variable
        # self.Seach()
        self.tableWidget.setRowCount(len(self.data))  # Number of rows based on JSON keys
                
        self.loadtable()  # Call the function to populate the table
        adjicon = qta.icon('ei.adjust-alt')
        self.advsearchbtn.setIcon(adjicon)
        self.advsearchbtn.clicked.connect(self.showadvsearchdig)
        self.lineeditsearch.returnPressed.connect(self.Seach)

    def tablestyle(self):
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        column_widths = [300,600,100,300,100]  # Widths for each column
        for col, width in enumerate(column_widths):
            self.tableWidget.setColumnWidth(col, width)
    # Add 'self' so it becomes an instance method
    def load_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def loadtable(self):
        if isinstance(self.data, list):  # Ensure JSON is a list
                self.tableWidget.setRowCount(len(self.data))  # Set row count

                for row, entry in enumerate(self.data):
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(entry.get("Name", "N/A")))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(entry.get("Path", "N/A")))
                    self.tableWidget.setItem(row, 2, QTableWidgetItem(entry.get("Type", "N/A")))
                    self.tableWidget.setItem(row, 3, QTableWidgetItem(entry.get("Modification Time", "N/A")))  # Match JSON key
                    self.tableWidget.setItem(row, 4, QTableWidgetItem(str(entry.get("Size (bytes)", "N/A"))))  # Match JSON key
        else:
            print("Error: JSON data is not a list.")

    def showadvsearchdig(self, checked):
        if self.w is None:
            self.w = loaddialogs.loadadvseach()
            # lonewin.exec_()
        self.w.show()

    def Seach(self):
        serach_text(str(self.lineeditsearch.text()))

app = QtWidgets.QApplication(sys.argv)
apply_stylesheet(app, theme='dark_amber.xml')

window = MainWindow()
window.show()
app.exec()
