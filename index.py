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
        self.server = MuseServer(self)
        self.server.start()
        self.eeg_readings = {}
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

        self.pw = pg.PlotWidget()
        self.setCentralWidget(self.pw)

        self.show()
    def updateAcc(self):
        pass
    
    def updateEEG(self, l_ear, l_forehead, r_forehead, r_ear):
        self.eeg_readings['alpha'] = np.roll(self.eeg_readings['alpha'], -1)
        self.eeg_readings['alpha'][-1] = l_ear/100.
        self.alphaPlot.setData(self.eeg_readings['alpha'])

def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
