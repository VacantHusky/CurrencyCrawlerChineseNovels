from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class AboutWidget(QWidget):
    title = '关于本软件'
    about = '''
    免责声明：
    本软件属于个人的非赢利性软件。由本软件产生的一切数据均来自于互联网，
    本软件不保证其真实性。得到的数据（txt）可能会侵害他人的权益。
    请务必在下载后24小时内删除。
    ================================
    GitHub:
    作者：TigerWang
    邮箱：conan1015@foxmail.com
    博客：www.hbmu.xyz'''
    def __init__(self):
        super().__init__()
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout_about")

        self.label_title = QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(31)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.verticalLayout.addWidget(self.label_title, 0, QtCore.Qt.AlignHCenter)

        self.label_about = QLabel(self)
        self.label_about.setObjectName("label_about")
        self.verticalLayout.addWidget(self.label_about, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 4)

        _translate = QtCore.QCoreApplication.translate
        self.label_title.setText(_translate("MainWindow", self.title))
        self.label_about.setText(_translate("MainWindow", self.about))

