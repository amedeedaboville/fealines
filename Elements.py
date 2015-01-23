import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from functools import partial
import muselo

class EEGPlot:
    def __init__(self, signals):
        self.pw = pg.PlotWidget()
        self.data = {}
        self.plots = {}
        lines = set()
        bands = ['alpha', 'beta', 'delta', 'gamma', 'theta']

        for sig in signals.split(","):
            signal_name = self.read_signal(sig)
            lines = lines.union(signal_name)

        for line in lines:
            self.data[line] = np.random.normal(size=100)
            self.plots[line] = self.pw.plot(title=line, y=self.data[line], pen=(0, 255, 0, 100))

            if line == 'fea':
                muselo.server.register_listener('/muse/elements/alpha_relative', self.receive_fea)
            else:
                band_name = signal_name[:-1]
                if band_name in bands:
                    muselo.server.register_listener('/muse/elements/%s_relative' % band_name, partial(self.receive_band, line=signal_name))
                else:
                    raise KeyError("Couldn't understand signal name %s and didn't register with server" % signal_name)
        # self.lines = lines

    def receive_band(self, line, args):
        print line
        signal_number = int(line[-1])
        new_dp = args[signal_number]
        self.update_dp(line, new_dp)

    def receive_fea(self, args):
        print "receiving fea dp "
        left_alpha = args[1]
        right_alpha = args[2]
        new_dp = right_alpha - left_alpha
        self.update_dp('fea', new_dp)

    def update_dp(self, line, new_dp):
        self.data[line] = np.roll(self.data[line], -1)
        self.data[line][-1] = new_dp/100.
        self.plots[line].setData(self.data[line])

    @classmethod
    def read_signal(cls, sig):
        bands = ['alpha', 'beta', 'gamma', 'delta', 'theta']
        locations = ['0', '1', '2', '3']
        sides_lr = {'right': ['2', '3'], 'left': ['0', '1']}
        sides_fb= {'front': ['1', '2'], 'frontal': ['1','2'], 'back': ['0', '3'], 'ears': ['0','3']}

        signals = {}
        signals['all'] = set([band + loc for loc in locations for band in bands])

        for side, locs in sides_fb.iteritems(): # front-alpha
            for band in bands:
                signals[side + '-' + band] = set([band + loc for loc in locs])

        for side, locs in sides_lr.iteritems(): # right-beta
            for band in bands:
                signals[side + '-' + band] = set([band + loc for loc in locs])

        for fb in sides_fb: #back-left-gamma
            for lr in sides_lr:
                for band in bands:
                    signals[fb + '-' + lr + '-' + band] = signals[fb + '-' + band].intersection(signals[lr + '-' + band])

        return signals[sig]


class TimerWidget(QtGui.QLabel):

    def __init__(self, time, callback):
        """
        :param time:
        The duration of the countdown timer, in seconds
        :param callback:
        The callback for when the timer finishes
        """
        super(TimerWidget, self).__init__()

        self.setText("%d:%02d" % (time/60., time % 60))

        self.time_left = time
        self.total_timer = QtCore.QTimer(self)
        self.total_timer.timeout.connect(callback)
        self.total_timer.start(time * 1000)

        self.seconds_timer = QtCore.QTimer(self)
        self.seconds_timer.timeout.connect(self.updateDisplay)
        self.seconds_timer.start(1000)

    def updateDisplay(self):
        self.time_left -= 1
        self.setText("%d:%02d" % (self.time_left/60., self.time_left % 60))

