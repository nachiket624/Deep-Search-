from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from Mainwindow.Dialogs import advsearch
import qtawesome as qta

class loadadvseach(QtWidgets.QDialog,advsearch.Ui_Dialog):
    def __init__(self):
        super(loadadvseach, self).__init__()
        self.setupUi(self)
        adjicon = qta.icon('fa5s.search')
        self.digadvsearchbtn.setIcon(adjicon)