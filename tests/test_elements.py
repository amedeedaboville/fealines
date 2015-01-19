from enaml.qt.qt_widget import QtWidget
from Elements import EEGPlot


class TestElements:

    def testEegPlot(self):
        plot = EEGPlot()
        controls = plot.getControlWidget()
        assert isinstance(controls, QtWidget)
        assert isinstance(plot.getWidget(), QtWidget)
