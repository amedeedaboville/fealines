import numpy as np
import pyqtgraph as pg
from functools import partial
import muselo


class EEGPlot:
    def __init__(self, plot_params):
        pg.setConfigOption('background', 'w')
        self.pw = pg.PlotWidget(pen=pg.mkPen('b', width=4))
        self.bar_color = (100,100,255)
        self.data = {}# All of the data points ever received
        self.plot_data = {}# The datapoints that are shown on the screen
        self.plots = {}
        self.lines = set()
        self.listeners = []
        plot_params.setdefault("type", "bar")
        if plot_params['type'] == "bar":
            self.bar = True
            self.bar_buffer = {} # A buffer that holds datapoints until they are averaged into bars
            self.dp_counter = {} # The number of datapoints in the buffer so far
            if 'bar_width' in plot_params:
                self.bar_width = int(plot_params['bar_width'])
            else:
                self.bar_width = 15
        else:
            self.bar = False

        print "'", plot_params['signals'], "'"
        for sig in plot_params['signals'].split(","):
            signal_name = self.read_signal(sig)
            self.lines = self.lines.union(signal_name)

    def start(self):
        bands = ['alpha', 'beta', 'delta', 'gamma', 'theta']
        for line in self.lines:
            self.data[line] = []
            self.plot_data[line] = [np.arange(100), np.zeros(100)]
            if self.bar:
                self.bar_buffer[line] = np.zeros(self.bar_width)
                self.dp_counter[line] = 0
                self.plots[line] = self.pw.plot(title=line, x=self.plot_data[line][0], y=self.plot_data[line][1],
                                                fillLevel=0, fillBrush=self.bar_color)
            else:
                self.plots[line] = self.pw.plot(title=line, x=self.plot_data[line][0], y=self.plot_data[line])


            #For now we register listeners on the paths of both muse-player versions: 3.4 and 3.6
            if line == 'fea':
                self.register_muse_listener('/muse/elements/alpha_relative', self.receive_fea)
                self.register_muse_listener('/muse/dsp/elements/alpha', self.receive_fea)
            else:
                band_name = line[:-1]
                if band_name in bands:
                    self.register_muse_listener('/muse/elements/%s_relative'%band_name, partial(self.receive_band,line))
                    self.register_muse_listener('/muse/dsp/elements/%s' % band_name, partial(self.receive_band, line))
                else:
                    raise KeyError("Couldn't understand signal name %s and didn't register with server" % line)

    def register_muse_listener(self, path, callback):  # Record listeners here so we can remove them later
        self.listeners.append((path, callback))
        muselo.server.register_listener(path, callback)

    def stop(self):
        for path,callback in self.listeners:
            muselo.server.remove_listener(path, callback)

    def get_widget(self):
        return self.pw

    def receive_band(self, line, path, args):
        signal_number = int(line[-1])
        new_dp = args[signal_number]  # args is [band_name, [left_ear, left_forehead, right_forehead, right_ear]]
        self.update_dp(line, new_dp)

    def receive_fea(self, path, args):
        left_alpha = args[1]
        right_alpha = args[2]

        new_dp = right_alpha - left_alpha
        self.update_dp('fea', new_dp)

    def update_dp(self, line, new_dp):
        self.data[line].append(new_dp)

        if self.bar:
            idx = self.dp_counter[line]
            print idx
            if idx < self.bar_width:
                self.bar_buffer[line][idx] = new_dp
                self.dp_counter[line] += 1
            else:
                print "ignoring dp"

            if idx >= self.bar_width:
                avg = self.bar_buffer[line].mean()
                self.dp_counter[line] = 0
                self.bar_buffer[line][:] = 0

                roll_amount = -1 * (self.bar_width + 1)
                last_x = self.plot_data[line][0][-1]
                self.plot_data[line][0] = np.roll(self.plot_data[line][0], roll_amount) # remove points off the left

                self.plot_data[line][0][roll_amount:-1] = np.arange(last_x, last_x + self.bar_width)
                self.plot_data[line][0][-1] = self.plot_data[line][0][-2] + 0.1

                self.plot_data[line][1] = np.roll(self.plot_data[line][1], roll_amount) # remove points off the left
                self.plot_data[line][1][roll_amount:-1] = avg #add x points (our bar) on the right
                self.plot_data[line][1][-1] = 0  # We need this for the bar to look straight

                self.plots[line].setData(x=self.plot_data[line][0], y=self.plot_data[line][1])
        else:
            self.plot_data[line][1] = np.roll(self.plot_data[line][1], -1) # remove points off the left
            self.plot_data[line][1] = np.roll(self.plot_data[line][1], -1) # remove points off the left
            self.plots[line].setData(x=self.plot_data[line][0], y=self.plot_data[line][1])


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
