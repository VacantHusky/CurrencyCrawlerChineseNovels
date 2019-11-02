# import threading

from PyQt5.QtCore import QThread

# from settings import IS_QT5

# 这不能是一个线程
class SearchShow(QThread):
    tab = None
    def __init__(self,web, queue):
        super().__init__()
        self.web = web
        self.queue = queue

    def run(self):
        pass
        # books = self.queue.get()
        # if books == 'error' or books == 'over':
        #     return
        #
        # if IS_QT5:
        #     self.showQT5(books)
        # else:
        #     self.showCMD(books)
        #
        # # 正常退出
        # if self.queue.get() == 'over':
        #     pass

    def showQT5(self, books):
        # from UI.MyTabWidget import MyTabWidget
        # tab = MyTabWidget()
        # self.tab().add_ResultWidget(self.web,books)
        pass

    def showCMD(self, books):
        print('============={}的搜索结果================'.format(self.web))
        for book in books:
            print(book)
        print('\n\n')




