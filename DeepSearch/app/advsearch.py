# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'advsearch.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDateEdit, QDialog, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(814, 585)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.excludewords = QLineEdit(self.frame)
        self.excludewords.setObjectName(u"excludewords")

        self.horizontalLayout_6.addWidget(self.excludewords)


        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.fileexactphrasematchcase = QCheckBox(self.frame)
        self.fileexactphrasematchcase.setObjectName(u"fileexactphrasematchcase")

        self.horizontalLayout_7.addWidget(self.fileexactphrasematchcase)

        self.fileexactmactchwholeword = QCheckBox(self.frame)
        self.fileexactmactchwholeword.setObjectName(u"fileexactmactchwholeword")

        self.horizontalLayout_7.addWidget(self.fileexactmactchwholeword)

        self.fileexactmatchdiacribcs = QCheckBox(self.frame)
        self.fileexactmatchdiacribcs.setObjectName(u"fileexactmatchdiacribcs")

        self.horizontalLayout_7.addWidget(self.fileexactmatchdiacribcs)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)


        self.gridLayout.addLayout(self.verticalLayout_7, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.startdate = QDateEdit(self.frame)
        self.startdate.setObjectName(u"startdate")
        self.startdate.setWrapping(True)
        self.startdate.setFrame(False)
        self.startdate.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.startdate.setCalendarPopup(True)

        self.verticalLayout_2.addWidget(self.startdate)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.enddate = QDateEdit(self.frame)
        self.enddate.setObjectName(u"enddate")
        self.enddate.setWrapping(True)
        self.enddate.setFrame(False)
        self.enddate.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.enddate.setCalendarPopup(True)
        self.enddate.setDate(QDate(2099, 1, 1))

        self.verticalLayout_3.addWidget(self.enddate)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 1)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.size = QLabel(self.frame_2)
        self.size.setObjectName(u"size")
        self.size.setStyleSheet(u"font: 700 10pt \"Segoe UI\";")

        self.gridLayout_2.addWidget(self.size, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_4.addWidget(self.label_9)

        self.fileminsize = QSpinBox(self.frame_2)
        self.fileminsize.setObjectName(u"fileminsize")
        self.fileminsize.setMaximum(999999999)

        self.verticalLayout_4.addWidget(self.fileminsize)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_8 = QLabel(self.frame_2)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout.addWidget(self.label_8)

        self.filemaxsize = QSpinBox(self.frame_2)
        self.filemaxsize.setObjectName(u"filemaxsize")
        self.filemaxsize.setMaximum(999999999)
        self.filemaxsize.setValue(999999999)

        self.verticalLayout.addWidget(self.filemaxsize)


        self.horizontalLayout_4.addLayout(self.verticalLayout)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 7, 0, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font: 700 10pt \"Segoe UI\";")

        self.verticalLayout_8.addWidget(self.label_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.phraseinput = QLineEdit(self.frame)
        self.phraseinput.setObjectName(u"phraseinput")

        self.horizontalLayout_9.addWidget(self.phraseinput)

        self.serchphrasebtn = QPushButton(self.frame)
        self.serchphrasebtn.setObjectName(u"serchphrasebtn")

        self.horizontalLayout_9.addWidget(self.serchphrasebtn)

        self.horizontalLayout_9.setStretch(0, 9)

        self.verticalLayout_8.addLayout(self.horizontalLayout_9)


        self.gridLayout.addLayout(self.verticalLayout_8, 3, 0, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.allthisword = QLineEdit(self.frame)
        self.allthisword.setObjectName(u"allthisword")

        self.horizontalLayout_2.addWidget(self.allthisword)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.filemachcase = QCheckBox(self.frame)
        self.filemachcase.setObjectName(u"filemachcase")

        self.horizontalLayout_3.addWidget(self.filemachcase)

        self.filematchwholeword = QCheckBox(self.frame)
        self.filematchwholeword.setObjectName(u"filematchwholeword")

        self.horizontalLayout_3.addWidget(self.filematchwholeword)

        self.filematchdiacribcs = QCheckBox(self.frame)
        self.filematchdiacribcs.setObjectName(u"filematchdiacribcs")

        self.horizontalLayout_3.addWidget(self.filematchdiacribcs)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout_6, 1, 0, 1, 1)

        self.modification = QLabel(self.frame)
        self.modification.setObjectName(u"modification")
        self.modification.setStyleSheet(u"font: 700 10pt \"Segoe UI\";")

        self.gridLayout.addWidget(self.modification, 5, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.filenameinput = QLineEdit(self.frame)
        self.filenameinput.setObjectName(u"filenameinput")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.filenameinput)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.fileextationinput = QComboBox(self.frame)
        self.fileextationinput.setObjectName(u"fileextationinput")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.fileextationinput)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"font: 700 10pt \"Segoe UI\";")

        self.verticalLayout_9.addWidget(self.label_11)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.filepathinput = QLineEdit(self.frame)
        self.filepathinput.setObjectName(u"filepathinput")

        self.horizontalLayout_8.addWidget(self.filepathinput)

        self.digadvborwesfile = QPushButton(self.frame)
        self.digadvborwesfile.setObjectName(u"digadvborwesfile")

        self.horizontalLayout_8.addWidget(self.digadvborwesfile)


        self.verticalLayout_9.addLayout(self.horizontalLayout_8)


        self.gridLayout.addLayout(self.verticalLayout_9, 4, 0, 1, 1)


        self.verticalLayout_5.addWidget(self.frame)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.digadvsearchbtn = QPushButton(Dialog)
        self.digadvsearchbtn.setObjectName(u"digadvsearchbtn")

        self.horizontalLayout_5.addWidget(self.digadvsearchbtn)

        self.digadvcancelbtn = QPushButton(Dialog)
        self.digadvcancelbtn.setObjectName(u"digadvcancelbtn")

        self.horizontalLayout_5.addWidget(self.digadvcancelbtn)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)


        self.gridLayout_3.addLayout(self.verticalLayout_5, 0, 0, 1, 1)

        QWidget.setTabOrder(self.filenameinput, self.fileextationinput)
        QWidget.setTabOrder(self.fileextationinput, self.allthisword)
        QWidget.setTabOrder(self.allthisword, self.filemachcase)
        QWidget.setTabOrder(self.filemachcase, self.filematchwholeword)
        QWidget.setTabOrder(self.filematchwholeword, self.filematchdiacribcs)
        QWidget.setTabOrder(self.filematchdiacribcs, self.excludewords)
        QWidget.setTabOrder(self.excludewords, self.fileexactphrasematchcase)
        QWidget.setTabOrder(self.fileexactphrasematchcase, self.fileexactmactchwholeword)
        QWidget.setTabOrder(self.fileexactmactchwholeword, self.fileexactmatchdiacribcs)
        QWidget.setTabOrder(self.fileexactmatchdiacribcs, self.phraseinput)
        QWidget.setTabOrder(self.phraseinput, self.serchphrasebtn)
        QWidget.setTabOrder(self.serchphrasebtn, self.filepathinput)
        QWidget.setTabOrder(self.filepathinput, self.digadvborwesfile)
        QWidget.setTabOrder(self.digadvborwesfile, self.startdate)
        QWidget.setTabOrder(self.startdate, self.enddate)
        QWidget.setTabOrder(self.enddate, self.fileminsize)
        QWidget.setTabOrder(self.fileminsize, self.filemaxsize)
        QWidget.setTabOrder(self.filemaxsize, self.digadvsearchbtn)
        QWidget.setTabOrder(self.digadvsearchbtn, self.digadvcancelbtn)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"None of These Words:", None))
        self.fileexactphrasematchcase.setText(QCoreApplication.translate("Dialog", u"Match case", None))
        self.fileexactmactchwholeword.setText(QCoreApplication.translate("Dialog", u"Match whole words", None))
        self.fileexactmatchdiacribcs.setText(QCoreApplication.translate("Dialog", u"Match diacribcs", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"From", None))
        self.startdate.setDisplayFormat(QCoreApplication.translate("Dialog", u"yyyy/M/d", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"To", None))
        self.enddate.setDisplayFormat(QCoreApplication.translate("Dialog", u"yyyy/M/d", None))
        self.size.setText(QCoreApplication.translate("Dialog", u"File Size", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"From (Bytes)", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"To (Bytes)", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"A word or phrase in the file:", None))
        self.serchphrasebtn.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"All This Words", None))
        self.filemachcase.setText(QCoreApplication.translate("Dialog", u"Match case", None))
        self.filematchwholeword.setText(QCoreApplication.translate("Dialog", u"Match whole words", None))
        self.filematchdiacribcs.setText(QCoreApplication.translate("Dialog", u"Match diacribcs", None))
        self.modification.setText(QCoreApplication.translate("Dialog", u"Modification Date Between ", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"File Name", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"File Extension", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Loacated In:", None))
        self.digadvborwesfile.setText("")
        self.digadvsearchbtn.setText("")
        self.digadvcancelbtn.setText("")
    # retranslateUi

