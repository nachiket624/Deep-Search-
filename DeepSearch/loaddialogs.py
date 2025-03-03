from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from Mainwindow.Dialogs import advsearch
import qtawesome as qta

class loadadvseach(QtWidgets.QDialog,advsearch.Ui_Dialog):
    def __init__(self):
        super(loadadvseach, self).__init__()
        self.setupUi(self)
        browesfile = qta.icon('ph.folder-notch-open-fill',color="yellow")
        self.digadvborwesfile.setIcon(browesfile)
        adjicon = qta.icon('fa5s.search',color='green')
        self.digadvsearchbtn.setIcon(adjicon)
        cancelicon = qta.icon('mdi.cancel',color='red')
        self.digadvcancelbtn.setIcon(cancelicon)