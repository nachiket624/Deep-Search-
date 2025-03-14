from PySide6 import QtWidgets
from PySide6.QtWidgets import *
import sys
import json
from qt_material import apply_stylesheet
import qtawesome as qta

# ui element
from Mainwindow.MainWindow import Ui_MainWindow
import loaddialogs
from Modules.Search.simplesearch import search_files

def load_index(file_path):
    """Load file index from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: file_index.json not found.")
        return []
def main():
    file_index = load_index(r"../DeepSearch/Modules/Indexrecord/file_index.json")
    if not file_index:
        return
    print("Returning file_index")
    return file_index
    

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.w = None
        self.w1 = None
        self.setupUi(self)
        json_file = "../DeepSearch/Modules/Indexrecord/file_index.json"  # Ensure this file exists
        self.data = self.load_json(json_file)  # Store data in an instance variable
        self.tableWidget.setRowCount(len(self.data))  # Number of rows based on JSON keys
        # self.tablestyle() 
        self.update_table()  # Call the function to populate the table
        adjicon = qta.icon('ei.adjust-alt')
        self.advsearchbtn.setIcon(adjicon)
        self.advsearchbtn.clicked.connect(self.showadvsearchdig)
        self.lineeditsearch.returnPressed.connect(self.Seach)

    def tablestyle(self):
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        table_header = ["Name","Path","Type","Modification Time","Size (bytes)"]
        self.tableWidget.setHorizontalHeaderLabels(table_header)
        column_widths = [300,600,100,300,140]  # Widths for each column
        for col, width in enumerate(column_widths):
            self.tableWidget.setColumnWidth(col, width)
    # Add 'self' so it becomes an instance method
    def load_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def update_table(self):
        self.tablestyle()
        if self.tableWidget is None:
            return
        self.tableWidget.setRowCount(len(self.data))  # Set row count
        for row, entry in enumerate(self.data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(entry.get("Name", "N/A")))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(entry.get("Path", "N/A")))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(entry.get("Type", "N/A")))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(entry.get("Modification Time", "N/A")))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(entry.get("Size (bytes)", "N/A"))))

    def loadtable(self):
        if isinstance(self.data, list):  # Ensure JSON is a list
                self.tableWidget.setRowCount(len(self.data))  # Set row count
                for row, entry in enumerate(self.data):
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(entry.get("Name", "N/A")))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(entry.get("Path", "N/A")))
                    self.tableWidget.setItem(row, 2, QTableWidgetItem(entry.get("Type", "N/A")))
                    self.tableWidget.setItem(row, 3, QTableWidgetItem(entry.get("Modification Time", "N/A")))  # Match JSON key
                    self.tableWidget.setItem(row, 4, QTableWidgetItem(str(entry.get("Size (bytes)", "N/A"))))  # Match JSON key   
                self.tablestyle() 
        else:
            print("Error: JSON data is not a list.")
        

    def showadvsearchdig(self, checked):
        if self.w is None:
            self.w = loaddialogs.LoadAdvSearch()
        self.w.show()

    def Seach(self):
        file_index = main()      
        filename = (str(self.lineeditsearch.text()))
        print("File Name is ",filename)
        formatted_results = []
        results = search_files(file_index, name=filename, file_type=None, mod_date=None, size=None)
        if results:
            for res in results:
                formatted_results.append(res)
            self.tableWidget.clear()
            self.data = formatted_results
            self.loadtable()            
        else:
            dlg = QMessageBox(self)           
            dlg.setWindowTitle("Soory!")
            dlg.setText("No matching files found.")
            dlg.exec()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_purple.xml')
    window = MainWindow()
    window.show()
    app.exec()
