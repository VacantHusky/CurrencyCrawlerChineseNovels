from PyQt5 import QtCore, QtGui
from queue import Queue

import time
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QApplication

from crawler import Request

_translate = QtCore.QCoreApplication.translate


# 书籍列表面板
class BooksWidget(QWidget):
    bookwidgetlist = []

    def __init__(self, books, web):
        super().__init__()
        self.books = books
        self.web = web
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.add_books(self.books)

    def add_books(self, books):
        for book in books:
            self.add_book(book)

    # 列表中添加一本
    def add_book(self, book):
        widget_info = BookWidget(self, book, self.web)
        widget_info.setMinimumSize(QtCore.QSize(200, 100))
        widget_info.setMaximumSize(QtCore.QSize(16777215, 200))
        widget_info.setObjectName("widget_info")
        self.verticalLayout.addWidget(widget_info)
        self.bookwidgetlist.append(widget_info)


# 单本书籍面板
class BookWidget(QWidget):
    def __init__(self, parent, book, web):
        super().__init__(parent=parent)
        self.web = web
        self.set_gridLayout()
        self.set_image()
        self.set_title()
        self.set_author()
        self.set_info()
        self.set_read_button()
        self.set_save_button()
        self.set_grid2()
        self.set_text(book)

    def set_gridLayout(self, ):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

    def set_image(self):
        self.label_image = QLabel(self)
        self.label_image.setMinimumSize(QtCore.QSize(100, 100))
        self.label_image.setMaximumSize(QtCore.QSize(100, 200))
        self.label_image.setText("")
        self.label_image.setTextFormat(QtCore.Qt.AutoText)
        self.label_image.setScaledContents(True)
        self.label_image.setWordWrap(False)
        self.label_image.setOpenExternalLinks(False)
        self.label_image.setObjectName("label_image")
        self.gridLayout.addWidget(self.label_image, 1, 0, 3, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def set_title(self):
        self.label_title = QLabel(self)
        self.label_title.setObjectName("label_title")
        self.gridLayout.addWidget(self.label_title, 1, 1, 1, 1)

    def set_info(self):
        self.label_info = QLabel(self)
        self.label_info.setObjectName("label_info")
        self.gridLayout.addWidget(self.label_info, 3, 1, 1, 2, QtCore.Qt.AlignTop)

    def set_author(self):
        self.label_author = QLabel(self)
        self.label_author.setObjectName("label_author")
        self.gridLayout.addWidget(self.label_author, 2, 1, 1, 1)

    def set_save_button(self):
        self.saveButton = QPushButton(self)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setMinimumSize(QtCore.QSize(100, 10))
        self.saveButton.setMaximumSize(QtCore.QSize(100, 20))
        self.gridLayout.addWidget(self.saveButton, 1, 2, 1, 1)

        # 绑定save按钮事件
        self.saveButton.clicked.connect(self.click_button)

    def set_read_button(self):
        self.readButton = QPushButton(self)
        self.readButton.setObjectName("readButton")
        self.readButton.setMinimumSize(QtCore.QSize(100, 10))
        self.readButton.setMaximumSize(QtCore.QSize(100, 20))
        self.gridLayout.addWidget(self.readButton, 2, 2, 1, 1)

        # 绑定read按钮事件
        self.readButton.clicked.connect(lambda :self.readButton.setText('此功能还未开发'))

    def set_grid2(self):
        self.gridLayout.setColumnMinimumWidth(0, 1)
        self.gridLayout.setColumnMinimumWidth(1, 3)
        self.gridLayout.setColumnMinimumWidth(2, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 1)

    def set_text(self, book):
        self.book = book
        book.info_intact = book.info
        img = QImage(book.image)
        if 'http' in book.image:
            img = 'image/default.jpg'
        self.label_image.setPixmap(QtGui.QPixmap.fromImage(img))
        self.label_title.setText(_translate("MainWindow", "《{}》".format(book.title)))
        self.label_author.setText(
            _translate("MainWindow", "{} | {} | {}字".format(book.author, book.genre, book.word_n)))
        info = book.info
        info = info.replace('\n', ' ')
        if len(info) > 120:
            info = info[:60] + '\n' + info[60:120]
        elif len(info) > 60:
            info = info[:60] + '\n' + info[60:]
        else:
            info = info + '　' * (60 - len(info))
        self.label_info.setText(_translate("MainWindow", "简介：\n{}".format(info)))
        self.readButton.setText(_translate("MainWindow", "阅读"))
        self.saveButton.setText(_translate("MainWindow", "下载txt"))


    def click_button(self):
        self.saveButton.setText(_translate("MainWindow", "下载中..."))
        queue = Queue()
        print('aaaa'+self.web)
        Request().createDownTxt(self.web,self.book,queue)
        is_ok = True
        while 1:
            if queue.empty():
                QApplication.processEvents()
                continue
            id, chapter = queue.get()
            if id == 'over' or chapter == 'over':
                print(chapter)
                break
            if id == '404':
                is_ok = False
                break
            if id < -1:
                self.saveButton.setText(_translate("MainWindow", "剩余{}".format(-id)))
            else:
                self.saveButton.setText(_translate("MainWindow", "正在保存.."))
        if is_ok:
            self.saveButton.setText(_translate("MainWindow", "下载完成"))
            QApplication.processEvents()
            time.sleep(5)
        else:
            self.saveButton.setText(_translate("MainWindow", "下载失败"))
            QApplication.processEvents()
            time.sleep(5)
        self.saveButton.setText(_translate("MainWindow", "重新下载"))
