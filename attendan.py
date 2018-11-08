# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'attendan.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(206, 217, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 301, 761, 261))
        self.textBrowser.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 250, 261, 41))
        self.pushButton.setStyleSheet("background-color: rgb(188, 255, 244);")
        self.pushButton.setObjectName("pushButton")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(50, 100, 89, 16))
        self.radioButton.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.radioButton.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(50, 130, 71, 17))
        self.radioButton_2.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.radioButton_2.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.radioButton_2.setObjectName("radioButton_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 50, 131, 181))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(170, 50, 251, 181))
        self.groupBox_3.setObjectName("groupBox_3")
        self.utime = QtWidgets.QTimeEdit(self.groupBox_3)
        self.utime.setGeometry(QtCore.QRect(110, 40, 118, 22))
        self.utime.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"selection-color: rgb(85, 170, 0);\n"
"selection-background-color: rgb(177, 177, 177);")
        self.utime.setTime(QtCore.QTime(9, 0, 0))
        self.utime.setObjectName("utime")
        self.dtime = QtWidgets.QTimeEdit(self.groupBox_3)
        self.dtime.setGeometry(QtCore.QRect(110, 80, 118, 22))
        self.dtime.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"selection-color: rgb(85, 170, 0);\n"
"selection-background-color: rgb(177, 177, 177);")
        self.dtime.setTime(QtCore.QTime(18, 0, 0))
        self.dtime.setObjectName("dtime")
        self.otime = QtWidgets.QTimeEdit(self.groupBox_3)
        self.otime.setGeometry(QtCore.QRect(110, 120, 118, 22))
        self.otime.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"selection-color: rgb(85, 170, 0);\n"
"selection-background-color: rgb(177, 177, 177);")
        self.otime.setTime(QtCore.QTime(9, 30, 0))
        self.otime.setObjectName("otime")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(20, 40, 71, 21))
        self.label_3.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 71, 21))
        self.label_4.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(20, 120, 71, 21))
        self.label_5.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.label_5.setObjectName("label_5")
        self.cyear = QtWidgets.QSpinBox(self.centralwidget)
        self.cyear.setGeometry(QtCore.QRect(110, 10, 61, 22))
        self.cyear.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"selection-color: rgb(85, 170, 0);\n"
"selection-background-color: rgb(177, 177, 177);")
        self.cyear.setMinimum(2018)
        self.cyear.setMaximum(2028)
        self.cyear.setObjectName("cyear")
        self.cmonth = QtWidgets.QSpinBox(self.centralwidget)
        self.cmonth.setGeometry(QtCore.QRect(210, 10, 61, 22))
        self.cmonth.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"selection-color: rgb(85, 170, 0);\n"
"selection-background-color: rgb(177, 177, 177);")
        self.cmonth.setMinimum(1)
        self.cmonth.setMaximum(12)
        self.cmonth.setObjectName("cmonth")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label_6.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(180, 10, 21, 21))
        self.label_7.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(290, 10, 16, 21))
        self.label_8.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.label_8.setObjectName("label_8")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(450, 0, 331, 101))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(20, 10, 301, 21))
        self.label_9.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.label_9.setObjectName("label_9")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox_4)
        self.textEdit_2.setGeometry(QtCore.QRect(20, 40, 291, 41))
        self.textEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"selection-color: rgb(85, 170, 0);\n"
"selection-background-color: rgb(177, 177, 177);")
        self.textEdit_2.setObjectName("textEdit_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(450, 130, 331, 101))
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.label_10 = QtWidgets.QLabel(self.groupBox_5)
        self.label_10.setGeometry(QtCore.QRect(20, 10, 291, 21))
        self.label_10.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 10pt \"ADMUI3Lg\";")
        self.label_10.setObjectName("label_10")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_5)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 291, 41))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"selection-color: rgb(85, 170, 0);\n"
"selection-background-color: rgb(177, 177, 177);")
        self.textEdit.setObjectName("textEdit")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(140, 250, 91, 41))
        self.checkBox.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox.setObjectName("checkBox")
        self.groupBox_3.raise_()
        self.groupBox.raise_()
        self.textBrowser.raise_()
        self.pushButton.raise_()
        self.radioButton.raise_()
        self.radioButton_2.raise_()
        self.cyear.raise_()
        self.cmonth.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.groupBox_4.raise_()
        self.groupBox_5.raise_()
        self.checkBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName("menuhelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.menuhelp.addSeparator()
        self.menuhelp.addSeparator()
        self.menuhelp.addAction(self.action_2)
        self.menubar.addAction(self.menuhelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "考勤管理系统"))
        self.pushButton.setText(_translate("MainWindow", "制作考勤"))
        self.radioButton.setText(_translate("MainWindow", "11层"))
        self.radioButton_2.setText(_translate("MainWindow", "23层"))
        self.groupBox.setTitle(_translate("MainWindow", "考勤区域选择"))
        self.groupBox_3.setTitle(_translate("MainWindow", "上下班时间"))
        self.label_3.setText(_translate("MainWindow", "上班时间"))
        self.label_4.setText(_translate("MainWindow", "下班时间"))
        self.label_5.setText(_translate("MainWindow", "迟到时间"))
        self.label_6.setText(_translate("MainWindow", "考勤月份选择"))
        self.label_7.setText(_translate("MainWindow", "年"))
        self.label_8.setText(_translate("MainWindow", "月"))
        self.label_9.setText(_translate("MainWindow", "节假日 （元旦:2018-01-01 2018-01-03,号隔开）"))
        self.label_10.setText(_translate("MainWindow", "免打卡人员 （,号隔开）"))
        self.checkBox.setText(_translate("MainWindow", "统计加班"))
        self.menuhelp.setTitle(_translate("MainWindow", "help"))
        self.action_2.setText(_translate("MainWindow", "软件简介"))

