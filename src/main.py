import signal

from pyqtgraph.Qt import QtGui

from muselo import *
from Protocol.feaProtocol import Protocol, ProtocolNotLoaded

signal.signal(signal.SIGINT, signal.SIG_DFL)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        closeAction = QtGui.QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Application')
        closeAction.triggered.connect(quit)

        loadAction = QtGui.QAction('Load Protocol', self)
        loadAction.setStatusTip('Load the Default Protocol')
        loadAction.triggered.connect(self.executeProtocol)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu = menubar.addMenu('&Load')
        fileMenu.addAction(closeAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(closeAction)
        self.toolbar.addAction(loadAction)

        self.setGeometry(1000,1000,1000,1000)
        self.setWindowTitle('fealines')
        self.setCentralWidget(QtGui.QLabel("No protocol running"))
        self.show()


    def executeProtocol(self):
        try:
            self.pcl = Protocol('./protocols/default.json', self.protocolEnded)
            self.central_widget = self.pcl.main_widget
            self.pcl.start()
            self.setCentralWidget(self.central_widget)
        except ProtocolNotLoaded:
            pass

    def protocolEnded(self):
        self.setCentralWidget(QtGui.QLabel("No protocol loaded"))


def main():
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    # main.executeProtocol()
    app.exec_()
    sys.exit(0)

if __name__ == '__main__':
    main()
