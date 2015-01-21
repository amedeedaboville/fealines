import numpy as np
import pyqtgraph as pg
class EEGPlot:
    def __init__(self, signals):
        self.pw = pg.PlotWidget()

        self.data = {}
        lines =  [self.read_signal(sig) for sig in signals.split(",")]
        for line in lines:
            self.data[line] = np.random.normal(size=100)
            self.plots[line] = self.pw.plot(title=line, y=self.data[line], pen=(0, 255, 0, 100))
        #TODO: register callbacks for updates on the lines we are plotting
        return self.pw

    def update(self, signal, new_dp):
        self.data[signal] = np.roll(self.data[signal], -1)
        self.data[signal][-1] = new_dp/100.
        self.plots[signal].setData(self.data[signal])

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


class TimerWidget(QtGui.QWidget):

    def __init__(self, time, callback):
        """
        :param time:
        The duration of the countdown timer, in seconds
        :param callback:
        The callback for when the timer finishes
        """
        super(TimerWidget, self).__init__()

        self.label = QtGui.QLabel()

        self.time_left = time
        self.total_timer = QtCore.QTimer(self)
        self.total_timer.timeout.connect(callback)
        self.total_timer.start(time * 1000)

        self.seconds_timer = QtCore.QTimer(self)
        self.seconds_timer.timeout.connect(self.updateDisplay)
        self.seconds_timer.start(1000)

    def updateDisplay(self):
        self.time_left -= 1
        self.label.setText("%d:%02d" % (self.time_left/60., self.time_left % 60))

