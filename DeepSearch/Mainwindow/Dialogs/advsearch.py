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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QDateEdit,
    QDialog, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(833, 585)
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

        self.lineEdit_4 = QLineEdit(self.frame)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout_6.addWidget(self.lineEdit_4)


        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.checkBox_4 = QCheckBox(self.frame)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.horizontalLayout_7.addWidget(self.checkBox_4)

        self.checkBox_5 = QCheckBox(self.frame)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.horizontalLayout_7.addWidget(self.checkBox_5)

        self.checkBox_6 = QCheckBox(self.frame)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.horizontalLayout_7.addWidget(self.checkBox_6)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)


        self.gridLayout.addLayout(self.verticalLayout_7, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.dateEdit = QDateEdit(self.frame)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setWrapping(True)
        self.dateEdit.setFrame(False)
        self.dateEdit.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.verticalLayout_2.addWidget(self.dateEdit)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.dateEdit_2 = QDateEdit(self.frame)
        self.dateEdit_2.setObjectName(u"dateEdit_2")
        self.dateEdit_2.setWrapping(True)
        self.dateEdit_2.setFrame(False)
        self.dateEdit_2.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.verticalLayout_3.addWidget(self.dateEdit_2)


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

        self.spinBox_2 = QSpinBox(self.frame_2)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMaximum(999999999)

        self.verticalLayout_4.addWidget(self.spinBox_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_8 = QLabel(self.frame_2)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout.addWidget(self.label_8)

        self.spinBox = QSpinBox(self.frame_2)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(999999999)

        self.verticalLayout.addWidget(self.spinBox)


        self.horizontalLayout_4.addLayout(self.verticalLayout)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 7, 0, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"font: 700 10pt \"Segoe UI\";")

        self.verticalLayout_8.addWidget(self.label_5)

        self.lineEdit_5 = QLineEdit(self.frame)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.verticalLayout_8.addWidget(self.lineEdit_5)


        self.gridLayout.addLayout(self.verticalLayout_8, 3, 0, 1, 1)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit_3 = QLineEdit(self.frame)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_2.addWidget(self.lineEdit_3)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_3.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.frame)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_3.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.frame)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.horizontalLayout_3.addWidget(self.checkBox_3)


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

        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_2 = QLineEdit(self.frame)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_2)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"font: 700 10pt \"Segoe UI\";")

        self.verticalLayout_9.addWidget(self.label_11)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.lineEdit_6 = QLineEdit(self.frame)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.horizontalLayout_8.addWidget(self.lineEdit_6)

        self.digadvborwesfile = QPushButton(self.frame)
        self.digadvborwesfile.setObjectName(u"digadvborwesfile")

        self.horizontalLayout_8.addWidget(self.digadvborwesfile)


        self.verticalLayout_9.addLayout(self.horizontalLayout_8)

        self.checkBox_7 = QCheckBox(self.frame)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.verticalLayout_9.addWidget(self.checkBox_7)


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

        self.label_10 = QLabel(Dialog)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 0, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"This Exact Phrase:", None))
        self.checkBox_4.setText(QCoreApplication.translate("Dialog", u"Match case", None))
        self.checkBox_5.setText(QCoreApplication.translate("Dialog", u"Match whole words", None))
        self.checkBox_6.setText(QCoreApplication.translate("Dialog", u"Match diacribcs", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"From", None))
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("Dialog", u"yyyy/M/d", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"To", None))
        self.dateEdit_2.setDisplayFormat(QCoreApplication.translate("Dialog", u"yyyy/M/d", None))
        self.size.setText(QCoreApplication.translate("Dialog", u"File Size", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"To", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"From", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"A word or phrase in the file:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"All This Words", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"Match case", None))
        self.checkBox_2.setText(QCoreApplication.translate("Dialog", u"Match whole words", None))
        self.checkBox_3.setText(QCoreApplication.translate("Dialog", u"Match diacribcs", None))
        self.modification.setText(QCoreApplication.translate("Dialog", u"Modification Date Between ", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"File Name", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"File Extension", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"A word or phrase in the file:", None))
        self.digadvborwesfile.setText("")
        self.checkBox_7.setText(QCoreApplication.translate("Dialog", u"Include Sub Folder", None))
        self.digadvsearchbtn.setText("")
        self.digadvcancelbtn.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"-", None))
    # retranslateUi

