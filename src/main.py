import signal

from pyqtgraph.Qt import QtGui

from muselo import *
from Protocol.feaProtocol import Protocol

signal.signal(signal.SIGINT, signal.SIG_DFL)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        closeAction = QtGui.QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Application')
        closeAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(closeAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(closeAction)

        self.setGeometry(1000,1000,1000,1000)
        self.setWindowTitle('fealines')
        self.show()

    def executeProtocol(self):
        self.pcl = Protocol('./protocols/test.json')
        self.central_widget = self.pcl.start()
        self.setCentralWidget(self.central_widget)

def main():
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.executeProtocol()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
