"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import signal
import sys

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
        #fileMenu.addAction(exitAction)
        fileMenu.addAction(closeAction)
        
        self.setGeometry(300,300,300,300)
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
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

#pg.setConfigOptions(antialias=True) # Enable antialiasing for prettier plots
#
#p1 = win.addPlot(title="Basic array plotting", y=np.random.normal(size=100))
#
#p3 = win.addPlot(title="Drawing with points")
#p3.plot(np.random.normal(size=100), pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')
#
#win.nextRow()
#
#p5 = win.addPlot(title="Scatter plot, axis labels, log scale")
#x = np.random.normal(size=1000) * 1e-5
#y = x*1000 + 0.005 * np.random.normal(size=1000)
#y -= y.min()-1.0
#mask = x > 1e-15
#x = x[mask]
#y = y[mask]
#p5.plot(x, y, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
#
#p6 = win.addPlot(title="Updating plot")
#curve = p6.plot(pen='y')
#data = np.random.normal(size=(10,1000))
#ptr = 0
#def update():
#    global curve, data, ptr, p6
#    curve.setData(data[ptr%10])
#    if ptr == 0:
#        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
#    ptr += 1
#timer = QtCore.QTimer()
#timer.timeout.connect(update)
#timer.start(500)
#
#
#win.nextRow()
#
#x2 = np.linspace(-100, 100, 1000)
#data2 = np.sin(x2) / x2
#p8 = win.addPlot(title="Region Selection")
#p8.plot(data2, pen=(255,255,255,200))
#lr = pg.LinearRegionItem([400,700])
#lr.setZValue(-10)
#p8.addItem(lr)
#
#p9 = win.addPlot(title="Zoom on selected region")
#p9.plot(data2)
#def updatePlot():
#    p9.setXRange(*lr.getRegion(), padding=0)
#def updateRegion():
#    lr.setRegion(p9.getViewBox().viewRange()[0])
#lr.sigRegionChanged.connect(updatePlot)
#p9.sigXRangeChanged.connect(updateRegion)
#updatePlot()
