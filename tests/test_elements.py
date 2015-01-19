from enaml.qt.qt_widget import QtWidget
from Elements import EEGPlot


class TestElements:

    def testEegPlot(self):
        plot = EEGPlot('all')
        controls = plot.getControlWidget()
        assert isinstance(controls, QtWidget)
        assert isinstance(plot.getWidget(), QtWidget)

    def testSignalDescriptor(self):
        assert EEGPlot.read_signal('all') is not None

        assert EEGPlot.read_signal('frontal-alpha') is not None
        assert EEGPlot.read_signal('ear-gamma') is not None
        assert EEGPlot.read_signal('front-right-beta') is not None
        assert EEGPlot.read_signal('front-left-alpha') is not None

        assert EEGPlot.read_signal('alpha0') is not None
        assert EEGPlot.read_signal('beta1') is not None
        assert EEGPlot.read_signal('delta2') is not None
        assert EEGPlot.read_signal('gamma3') is not None
