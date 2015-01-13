from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import signal
import sys
from muselo import *

signal.signal(signal.SIGINT, signal.SIG_DFL)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.server = MuseServer()
        self.server.start()

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

        self.pw = pg.PlotWidget()
        self.setCentralWidget(self.pw)
        self.p1 = self.pw.plot(title="Basic array plotting", y=np.random.normal(size=100))

        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
