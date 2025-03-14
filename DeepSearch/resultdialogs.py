from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from Mainwindow.Dialogs import textresult

class loadtextresult(QtWidgets.QDialog,textresult.Ui_Dialog):
    def __init__(self):
        super(loadtextresult, self).__init__()
        self.setupUi(self)