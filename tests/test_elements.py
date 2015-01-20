from enaml.qt.qt_widget import QtWidget
from Elements import EEGPlot


class TestElements:

    def testEegPlot(self):
        plot = EEGPlot('all')
        assert isinstance(plot.getWidget(), QtWidget)

    def testSignalDescriptor(self):
        assert EEGPlot.read_signal('all') is not None

        assert EEGPlot.read_signal('frontal-alpha') == set(['alpha1', 'alpha2'])
        assert EEGPlot.read_signal('front-delta') == set(['delta1', 'delta2'])

        assert EEGPlot.read_signal('ears-beta') == set(['beta0', 'beta3'])
        assert EEGPlot.read_signal('back-gamma') == set(['gamma0', 'gamma3'])

        assert EEGPlot.read_signal('front-right-beta') == set(['beta2'])
        assert EEGPlot.read_signal('front-left-alpha') == set(['alpha1'])
