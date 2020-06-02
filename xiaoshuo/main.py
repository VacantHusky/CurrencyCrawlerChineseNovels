import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtWidgets
from UI import Ui_MainWindow

if __name__ == '__main__':
    ui = Ui_MainWindow()
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
