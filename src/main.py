import signal


from PyQt4.QtGui import QMainWindow, QAction, QLabel, QApplication
from muselo import *
from Protocol.feaProtocol import Protocol, ProtocolNotLoaded

signal.signal(signal.SIGINT, signal.SIG_DFL)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        closeAction = QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Application')
        closeAction.triggered.connect(lambda: sys.exit(0))

        loadAction = QAction('Load Protocol', self)
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
        self.setCentralWidget(QLabel("No protocol running"))
        self.show()


    def executeProtocol(self):
        print "Executing protocol"
        try:
            self.pcl = Protocol('./protocols/default.json', self.protocolEnded)
        except ProtocolNotLoaded:
            print "protocol not loaded..."
        self.central_widget = self.pcl.main_widget
        self.setCentralWidget(self.central_widget)
        self.pcl.start()

    def protocolEnded(self):
        self.setCentralWidget(QLabel("No protocol loaded"))


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.executeProtocol()
    app.exec_()
    sys.exit(0)

if __name__ == '__main__':
    main()
