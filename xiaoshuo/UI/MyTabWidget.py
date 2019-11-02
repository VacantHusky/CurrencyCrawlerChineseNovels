from PyQt5 import QtCore
from time import time, sleep

from PyQt5.QtWidgets import QTabWidget, QApplication

from UI.AboutWidget import AboutWidget
from UI.ResultWidget import ResultWidget
from UI.SearchWidget import SearchWidget
from UI.SetupWidget import SetupWidget
from crawler.showData import SearchShow
# from models import Book



_translate = QtCore.QCoreApplication.translate


class MyTabWidget(QTabWidget):
    result_list = []
    tab_setup = None
    tab_about = None

    # 单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if parent is not None:
            super().__init__(parent)
            self.parent_ = parent
            # 标签页-搜索
            self.tab_search = SearchWidget(self)
            self.tab_search.setObjectName("tab_search")
            self.addTab(self.tab_search, "")
            # 标签页-搜索结果
            # books = [
            #     Book(), Book(), Book(), Book(), Book(), Book(), Book(), Book(),
            # ]
            # self.add_ResultWidget(books=books)
            # self.open_setup()
            self.open_about()
            self.setCurrentIndex(self.indexOf(self.tab_search))

    def add_ResultWidget(self, web='空', books=[]):
        # 标签页-搜索结果
        tab = ResultWidget(web, books)
        tab.setObjectName("tab_{}".format(web))
        self.addTab(tab, "")
        self.result_list.append(tab)
        self.setTabText(self.indexOf(tab), _translate("MainWindow", web))
        self.setCurrentIndex(self.indexOf(tab))
        # self.tab = tab

    def add_ResultWidget_fuck(self, web, queue):
        start_time = time()
        while time() - start_time < 9:
            if queue.empty():
                QApplication.processEvents()
                continue
            web_, books = queue.get()
            if books == 'over':
                print('结束了！！！！')
                break
            assert web_ == web
            self.add_ResultWidget(web, books)
            # for book in books:
            #     print(book.title)
            #     print(book.info)
            break
        self.tab_search.searchButton.setText(_translate("MainWindow", "搜索"))

    def open_setup(self):
        if not self.tab_setup:
            self.tab_setup = SetupWidget()
            self.tab_setup.setObjectName("tab_setup")
            self.addTab(self.tab_setup, "")

    def open_about(self):
        if not self.tab_about:
            self.tab_about = AboutWidget()
            self.tab_about.setObjectName("tab_about")
            self.addTab(self.tab_about, "")

    def get_ResultWidget(self, web):
        for result in self.result_list:
            if result.getTabText()==web:
                return result

SearchShow.tab = MyTabWidget
