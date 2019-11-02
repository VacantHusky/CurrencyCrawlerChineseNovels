from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QScrollArea

from UI.BookWidget import BooksWidget

_translate = QtCore.QCoreApplication.translate


# 搜索结果页
class ResultWidget(QWidget):
    def __init__(self, web, books):
        super().__init__()
        self.web = web
        self.books = books
        self.set_gridLayout()
        self.set_label()
        self.set_scrollArea()
        self.set_bookswidget()
        self.label.setText(_translate("MainWindow", "{}搜索结果：".format(self.web)))

    def set_gridLayout(self):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

    def set_label(self):
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

    # 滚动面板
    def set_scrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)

    def set_bookswidget(self):
        # 书籍列表面板
        self.bookswidget = BooksWidget(self.books,self.web)
        self.bookswidget.setGeometry(QtCore.QRect(0, 0, 792, 510))
        self.bookswidget.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.bookswidget)
