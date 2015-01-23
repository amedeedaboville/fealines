from enaml.qt.qt_widget import QtWidget
import muselo
from Elements import EEGPlot


class TestElements:

    def testEegPlotSetup(self):
        plot = EEGPlot('all')
        assert isinstance(plot.getWidget(), QtWidget)

    def testEegPlotUpdate(self):
        plot = EEGPlot('all')
        assert muselo.server.listeners is not None  # check we have listeners (maybe move to a separate test_muselo?)
        assert plot in muselo.server.listeners['alpha1']  # check we are listening to specific messages

        plot.update('alpha1', 80)
        assert plot.data['alpha1'][-1] == 80
        # TODO: test long term storage of the plot's data

    def testSignalDescriptor(self):
        assert EEGPlot.read_signal('all') is not None

        assert EEGPlot.read_signal('frontal-alpha') == set(['alpha1', 'alpha2'])
        assert EEGPlot.read_signal('front-delta') == set(['delta1', 'delta2'])

        assert EEGPlot.read_signal('ears-beta') == set(['beta0', 'beta3'])
        assert EEGPlot.read_signal('back-gamma') == set(['gamma0', 'gamma3'])

        assert EEGPlot.read_signal('front-right-beta') == set(['beta2'])
        assert EEGPlot.read_signal('front-left-alpha') == set(['alpha1'])
