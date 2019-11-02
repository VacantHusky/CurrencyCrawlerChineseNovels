from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QCheckBox, QLabel, QPushButton, QLineEdit

from crawler import Request
from settings import WEB_NAME

_translate = QtCore.QCoreApplication.translate


class SearchWidget(QWidget):
    checkBoxList = []
    webs = WEB_NAME

    def __init__(self, tabtab):
        super().__init__()
        self.tabtab = tabtab
        self.set_searchLayout()
        self.set_searchLabel()
        self.set_searchEdit()
        self.set_searchButton()
        self.set_urlBox()

        self.searchLayout.setStretch(0, 2)
        self.searchLayout.setStretch(1, 3)
        self.searchLayout.setStretch(2, 2)
        self.searchLayout.setStretch(3, 2)

        self.set_text()

    def set_searchLayout(self):
        self.searchLayout = QVBoxLayout(self)
        self.searchLayout.setContentsMargins(0, 30, 0, 0)
        self.searchLayout.setSpacing(10)
        self.searchLayout.setObjectName("searchLayout")

    def searchLayout_add(self, obj):
        self.searchLayout.addWidget(obj, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

    def set_searchLabel(self):
        self.searchLabel = QLabel(self)
        self.searchLabel.setEnabled(True)
        self.searchLabel.setMinimumSize(QtCore.QSize(200, 100))
        self.searchLabel.setMaximumSize(QtCore.QSize(600, 100))
        self.searchLabel.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(37)
        self.searchLabel.setFont(font)
        self.searchLabel.setObjectName("searchLabel")
        self.searchLayout_add(self.searchLabel)

    def set_searchEdit(self):
        self.searchEdit = QLineEdit(self)
        self.searchEdit.setMinimumSize(QtCore.QSize(300, 30))
        self.searchEdit.setMaximumSize(QtCore.QSize(600, 50))
        self.searchEdit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.searchEdit.setObjectName("searchEdit")
        self.searchLayout_add(self.searchEdit)

    def set_searchButton(self):
        self.searchButton = QPushButton(self)
        self.searchButton.setMinimumSize(QtCore.QSize(100, 30))
        self.searchButton.setMaximumSize(QtCore.QSize(300, 35))
        self.searchButton.setObjectName("searchButton")
        self.searchLayout_add(self.searchButton)

        # 绑定搜索按钮事件
        self.searchButton.clicked.connect(self.click_button)

    def click_button(self):
        self.searchButton.setText(_translate("MainWindow", "搜索中..."))
        search_word = self.searchEdit.text().strip()
        print('点击了按钮，开始搜索：{}'.format(search_word))
        r = Request()
        tabtab = self.tabtab
        # 遍历选中的web
        for i in range(min(len(self.webs), 10)):
            box = self.checkBoxList[i]
            if box.isChecked():
                print(box.text(), '开始搜索')
                queue = r.createSearchThread(box.text(), search_word)
                tabtab.add_ResultWidget_fuck(box.text(), queue)

    def set_urlBox(self):
        self.urlBox = QGroupBox(self)
        self.urlBox.setObjectName("urlBox")
        self.gridLayout = QGridLayout(self.urlBox)
        self.gridLayout.setObjectName("gridLayout")

        for y in range(2):
            for x in range(5):
                checkBox = QCheckBox(self.urlBox)
                checkBox.setObjectName("checkBox_{}_{}".format(x, y))
                self.gridLayout.addWidget(checkBox, y, x, 1, 1)
                self.checkBoxList.append(checkBox)
        self.searchLayout_add(self.urlBox)

    def set_text(self):
        self.searchLabel.setText(_translate("MainWindow", "小说下载器"))
        self.searchButton.setText(_translate("MainWindow", "搜索"))
        self.urlBox.setTitle(_translate("MainWindow", "选择搜索网站"))
        webs = self.webs
        webs_len = len(webs)
        for i in range(10):
            if i < webs_len:
                self.checkBoxList[i].setText(_translate("MainWindow", webs[i]))
                self.checkBoxList[i].setChecked(True)  # 选中它！
            else:
                self.checkBoxList[i].setText(_translate("MainWindow", 'null'))
                self.checkBoxList[i].setEnabled(False)
