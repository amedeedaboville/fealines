from elements.EEGPlot import EEGPlot
import sys
from pyqtgraph.Qt import QtGui
from pyqtgraph.widgets.PlotWidget import PlotWidget
import numpy as np

app = QtGui.QApplication(sys.argv)
def test_eegplot_setup():
    plot = EEGPlot('all')
    assert isinstance(plot.get_widget(), PlotWidget)

def test_eegplot_update():
    print "testing update"
    plot = EEGPlot('all')
    plot.start()
    plot.receive_band('theta1', ('/muse/dsp/elements/theta', [0.1, 0.2, 0.3, 0.4]))
    print plot.data['theta1'][-1]
    assert plot.data['theta1'][-1] == 0.2
    # TODO: test long term storage of the plot's data

def test_receive_fea():
    plot = EEGPlot('fea')
    plot.start()
    plot.receive_fea('/muse/dsp/elements/alpha', [0.1, 0.2, 0.3, 0.4])
    assert np.isclose(plot.data['fea'][-1],0.1)
    plot.receive_fea('/muse/dsp/elements/alpha', [0.1, 0.3, 0.1, 0.4])
    assert np.isclose(plot.data['fea'][-1],-0.2)
    plot.receive_fea('/muse/dsp/elements/alpha', [0.1, 0.6, 0.6, 0.4])
    assert np.isclose(plot.data['fea'][-1],0)

def test_signal_descriptor():
    assert EEGPlot.read_signal('all') is not None

    assert EEGPlot.read_signal('frontal-alpha') == set(['alpha1', 'alpha2'])
    assert EEGPlot.read_signal('front-delta') == set(['delta1', 'delta2'])

    assert EEGPlot.read_signal('ears-beta') == set(['beta0', 'beta3'])
    assert EEGPlot.read_signal('back-gamma') == set(['gamma0', 'gamma3'])

    assert EEGPlot.read_signal('front-right-beta') == set(['beta2'])
    assert EEGPlot.read_signal('front-left-alpha') == set(['alpha1'])

def test_save():
    plot = EEGPlot('fea')
    plot.start()
    for i in range(10):
        plot.receive_fea('/muse/dsp/elements/alpha', [0.1, np.random.random(), np.random.random(), 0.4])
    saved_plot = plot.serialize()
    assert saved_plot is not None
    restored_plot = EEGPlot.deserialize(saved_plot)
    assert np.allclose(restored_plot.data['fea'], plot.data['fea'])
