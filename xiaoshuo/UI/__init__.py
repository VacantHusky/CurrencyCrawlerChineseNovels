# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'XiaoShuo.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from .MyTabWidget import MyTabWidget
from .SearchWidget import SearchWidget
from .AboutWidget import AboutWidget
from .ResultWidget import ResultWidget
from .SetupWidget import SetupWidget

# 总体
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        # 主面板
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # 栅格
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        # 标签页组件
        self.tabWidget = MyTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        # 菜单
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu_search = QtWidgets.QMenu(self.menubar)
        self.menu_search.setObjectName("menu_search")
        self.menu_setup = QtWidgets.QMenu(self.menubar)
        self.menu_setup.setObjectName("menu_setup")
        self.menu_about = QtWidgets.QMenu(self.menubar)
        self.menu_about.setObjectName("menu_about")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_search.menuAction())
        self.menubar.addAction(self.menu_setup.menuAction())
        self.menubar.addAction(self.menu_about.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "小说下载器-www.hbmu.xyz"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidget.tab_search), _translate("MainWindow", "搜索"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidget.tab_setup), _translate("MainWindow", "设置"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidget.tab_about), _translate("MainWindow", "about"))

        self.menu_search.setTitle(_translate("MainWindow", "搜索"))
        self.menu_setup.setTitle(_translate("MainWindow", "设置"))
        self.menu_about.setTitle(_translate("MainWindow", "about"))
