import numpy as np
import pyqtgraph as pg
from functools import partial
import muselo


class EEGPlot:
    def __init__(self, signals):
        self.pw = pg.PlotWidget()
        self.data = {}# All of the data points ever received
        self.plot_data = {}# The datapoints that are shown on the screen
        self.plots = {}
        self.lines = set()
        self.listeners = []

        for sig in signals.split(","):
            signal_name = self.read_signal(sig)
            self.lines = self.lines.union(signal_name)

    def start(self):
        bands = ['alpha', 'beta', 'delta', 'gamma', 'theta']
        for line in self.lines:
            self.data[line] = []
            self.plot_data[line] = np.empty(100)
            self.plots[line] = self.pw.plot(title=line, y=self.plot_data[line], pen=(0, 255, 0, 100))

            #For now we register listeners on the paths of both muse-player versions: 3.4 and 3.6
            if line == 'fea':
                self.register_muse_listener('/muse/elements/alpha_relative', self.receive_fea)

                self.register_muse_listener('/muse/dsp/elements/alpha', self.receive_fea)
            else:
                band_name = line[:-1]
                if band_name in bands:
                    self.register_muse_listener('/muse/elements/%s_relative' % band_name,
                                                    partial(self.receive_band, line))
                    self.register_muse_listener('/muse/dsp/elements/%s' % band_name,
                                                    partial(self.receive_band, line))
                else:
                    raise KeyError("Couldn't understand signal name %s and didn't register with server" % line)

    def register_muse_listener(self, path, callback): #We use this function to record all of our listeners
        self.listeners.append((path, callback))
        muselo.server.register_listener(path, callback)

    def stop(self):
        for path,callback in self.listeners:
            muselo.server.remove_listener(path, callback)

    def get_widget(self):
        return self.pw

    def receive_band(self, line, args):
        signal_number = int(line[-1])
        new_dp = args[1][signal_number]  # args is [band_name, [left_ear, left_forehead, right_forehead, right_ear]]
        self.update_dp(line, new_dp)

    def receive_fea(self, path, args):
        left_alpha = args[1]
        right_alpha = args[2]

        new_dp = right_alpha - left_alpha
        self.update_dp('fea', new_dp)

    def update_dp(self, line, new_dp):
        self.data[line].append(new_dp)

        self.plot_data[line] = np.roll(self.plot_data[line], -1)
        self.plot_data[line][-1] = new_dp
        self.plots[line].setData(self.plot_data[line])

    def serialize(self):
        plot_dict = {
            "lines": self.lines,
            "data": self.data
        }
        return plot_dict

    @classmethod
    def deserialize(cls, plot_dict):
        new_plot = EEGPlot('')
        new_plot.lines = plot_dict['lines']
        for key, value in plot_dict['data'].iteritems():
            print "adding key %s to data" % key
            new_plot.data[key] = value
        return new_plot

    @classmethod
    def read_signal(cls, sig):
        """

        :param sig: a name of a signal, like front-right-delta
        :return: a set of strings that are names of eeg bands
        """
        bands = ['alpha', 'beta', 'gamma', 'delta', 'theta']
        locations = ['0', '1', '2', '3']
        sides_lr = {'right': ['2', '3'], 'left': ['0', '1']}
        sides_fb = {'front': ['1', '2'], 'frontal': ['1', '2'], 'back': ['0', '3'], 'ears': ['0', '3']}

        signals = {}
        signals['all'] = set([band + loc for loc in locations for band in bands])
        signals['fea'] = set(('fea',))

        for side, locs in sides_fb.iteritems():  # front-alpha
            for band in bands:
                signals[side + '-' + band] = set([band + loc for loc in locs])

        for side, locs in sides_lr.iteritems():  # right-beta
            for band in bands:
                signals[side + '-' + band] = set([band + loc for loc in locs])

        for fb in sides_fb:  # back-left-gamma
            for lr in sides_lr:
                for band in bands:
                    signals[fb + '-' + lr + '-' + band] = signals[fb + '-' + band].intersection(
                        signals[lr + '-' + band])

        if sig in signals:
            return signals[sig]
        else:
            return ""
