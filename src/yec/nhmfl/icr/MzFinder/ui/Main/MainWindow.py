# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Thu May 28 16:38:26 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(753, 449)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtGui.QListWidget(self.groupBox)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_file_button = QtGui.QPushButton(self.groupBox)
        self.add_file_button.setObjectName("add_file_button")
        self.horizontalLayout.addWidget(self.add_file_button)
        self.delete_file_button = QtGui.QPushButton(self.groupBox)
        self.delete_file_button.setObjectName("delete_file_button")
        self.horizontalLayout.addWidget(self.delete_file_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeWidget = QtGui.QTreeWidget(self.groupBox_2)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_2.addWidget(self.treeWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_mz_button = QtGui.QPushButton(self.groupBox_2)
        self.add_mz_button.setObjectName("add_mz_button")
        self.horizontalLayout_2.addWidget(self.add_mz_button)
        self.delete_mz_button = QtGui.QPushButton(self.groupBox_2)
        self.delete_mz_button.setObjectName("delete_mz_button")
        self.horizontalLayout_2.addWidget(self.delete_mz_button)
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_4.addWidget(self.pushButton_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 753, 20))
        self.menubar.setObjectName("menubar")
        self.menuOpen = QtGui.QMenu(self.menubar)
        self.menuOpen.setObjectName("menuOpen")
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Thermo_raw = QtGui.QAction(MainWindow)
        self.actionOpen_Thermo_raw.setObjectName("actionOpen_Thermo_raw")
        self.menuOpen.addAction(self.actionOpen_Thermo_raw)
        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.add_file_button, QtCore.SIGNAL("released()"), MainWindow.add_file)
        QtCore.QObject.connect(self.delete_file_button, QtCore.SIGNAL("released()"), MainWindow.delete_file)
        QtCore.QObject.connect(self.add_mz_button, QtCore.SIGNAL("released()"), MainWindow.add_mz)
        QtCore.QObject.connect(self.delete_mz_button, QtCore.SIGNAL("released()"), MainWindow.delete_mz)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL("released()"), MainWindow.process_clicked)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("released()"), MainWindow.import_from_text_file)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MzFinder", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Selected Files", None, QtGui.QApplication.UnicodeUTF8))
        self.add_file_button.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_file_button.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Look for m/z: ", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "m/z", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "m/z window", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Abundance Threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.add_mz_button.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_mz_button.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Import from txt file ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("MainWindow", "Process", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOpen.setTitle(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Thermo_raw.setText(QtGui.QApplication.translate("MainWindow", "Open Thermo *.raw", None, QtGui.QApplication.UnicodeUTF8))


