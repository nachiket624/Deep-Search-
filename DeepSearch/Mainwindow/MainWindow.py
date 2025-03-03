# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1038, 503)
        MainWindow.setAnimated(False)
        self.actionView = QAction(MainWindow)
        self.actionView.setObjectName(u"actionView")
        self.actionMatch_Case = QAction(MainWindow)
        self.actionMatch_Case.setObjectName(u"actionMatch_Case")
        self.actionMatch_Case.setCheckable(True)
        self.actionMatch_Whole_Word = QAction(MainWindow)
        self.actionMatch_Whole_Word.setObjectName(u"actionMatch_Whole_Word")
        self.actionMatch_Whole_Word.setCheckable(True)
        self.actionMatch_Path = QAction(MainWindow)
        self.actionMatch_Path.setObjectName(u"actionMatch_Path")
        self.actionMatch_Path.setCheckable(True)
        self.actionEnable_Regex = QAction(MainWindow)
        self.actionEnable_Regex.setObjectName(u"actionEnable_Regex")
        self.actionEverything = QAction(MainWindow)
        self.actionEverything.setObjectName(u"actionEverything")
        self.actionEverything.setCheckable(True)
        self.actionEverything.setChecked(True)
        self.actionAudio = QAction(MainWindow)
        self.actionAudio.setObjectName(u"actionAudio")
        self.actionAudio.setCheckable(True)
        self.actionAudio.setChecked(False)
        self.actionDocument = QAction(MainWindow)
        self.actionDocument.setObjectName(u"actionDocument")
        self.actionDocument.setCheckable(True)
        self.actionDocument.setChecked(False)
        self.actionPicture = QAction(MainWindow)
        self.actionPicture.setObjectName(u"actionPicture")
        self.actionPicture.setCheckable(True)
        self.actionVideo = QAction(MainWindow)
        self.actionVideo.setObjectName(u"actionVideo")
        self.actionVideo.setCheckable(True)
        self.actionFolder = QAction(MainWindow)
        self.actionFolder.setObjectName(u"actionFolder")
        self.actionFolder.setCheckable(True)
        self.actionCompressed = QAction(MainWindow)
        self.actionCompressed.setObjectName(u"actionCompressed")
        self.actionCompressed.setCheckable(True)
        self.actionExecutable = QAction(MainWindow)
        self.actionExecutable.setObjectName(u"actionExecutable")
        self.actionExecutable.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineeditsearch = QLineEdit(self.centralwidget)
        self.lineeditsearch.setObjectName(u"lineeditsearch")

        self.horizontalLayout_2.addWidget(self.lineeditsearch)

        self.advsearchbtn = QPushButton(self.centralwidget)
        self.advsearchbtn.setObjectName(u"advsearchbtn")

        self.horizontalLayout_2.addWidget(self.advsearchbtn)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        if (self.tableWidget.rowCount() < 1):
            self.tableWidget.setRowCount(1)
        font = QFont()
        font.setPointSize(5)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font);
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem5)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget.setStyleSheet(u"")
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QFrame.Plain)
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setGridStyle(Qt.NoPen)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(10)
        self.tableWidget.verticalHeader().setDefaultSectionSize(60)
        self.tableWidget.verticalHeader().setHighlightSections(False)

        self.horizontalLayout.addWidget(self.tableWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1038, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuEdit_2 = QMenu(self.menubar)
        self.menuEdit_2.setObjectName(u"menuEdit_2")
        self.menuSearch = QMenu(self.menubar)
        self.menuSearch.setObjectName(u"menuSearch")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuEdit_2.menuAction())
        self.menubar.addAction(self.menuSearch.menuAction())
        self.menuSearch.addAction(self.actionMatch_Case)
        self.menuSearch.addAction(self.actionMatch_Whole_Word)
        self.menuSearch.addAction(self.actionMatch_Path)
        self.menuSearch.addSeparator()
        self.menuSearch.addAction(self.actionEnable_Regex)
        self.menuSearch.addSeparator()
        self.menuSearch.addAction(self.actionEverything)
        self.menuSearch.addAction(self.actionAudio)
        self.menuSearch.addAction(self.actionDocument)
        self.menuSearch.addAction(self.actionPicture)
        self.menuSearch.addAction(self.actionVideo)
        self.menuSearch.addAction(self.actionFolder)
        self.menuSearch.addAction(self.actionCompressed)
        self.menuSearch.addAction(self.actionExecutable)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionView.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.actionMatch_Case.setText(QCoreApplication.translate("MainWindow", u"Match Case", None))
        self.actionMatch_Whole_Word.setText(QCoreApplication.translate("MainWindow", u"Match Whole Word", None))
        self.actionMatch_Path.setText(QCoreApplication.translate("MainWindow", u"Match Path", None))
        self.actionEnable_Regex.setText(QCoreApplication.translate("MainWindow", u"Enable Regex", None))
        self.actionEverything.setText(QCoreApplication.translate("MainWindow", u"Everything", None))
        self.actionAudio.setText(QCoreApplication.translate("MainWindow", u"Audio", None))
        self.actionDocument.setText(QCoreApplication.translate("MainWindow", u"Document", None))
        self.actionPicture.setText(QCoreApplication.translate("MainWindow", u"Picture", None))
        self.actionVideo.setText(QCoreApplication.translate("MainWindow", u"Video", None))
        self.actionFolder.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.actionCompressed.setText(QCoreApplication.translate("MainWindow", u"Compressed", None))
        self.actionExecutable.setText(QCoreApplication.translate("MainWindow", u"Executable", None))
        self.advsearchbtn.setText("")
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Path", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Type", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Modification Date", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"size", None));
        ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuEdit_2.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuSearch.setTitle(QCoreApplication.translate("MainWindow", u"Search", None))
    # retranslateUi

