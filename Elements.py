
class EEGPlot:
    # self.bands = ['alpha', 'beta', 'gamma', 'delta', 'theta']
    # self.locations = ['0', '1', '2', '3']
    def __init__(self):
        self.eeg_readings['alpha'] = np.random.normal(size=100)
        self.eeg_readings['beta']  = np.random.normal(size=100)
        self.eeg_readings['delta'] = np.random.normal(size=100)
        self.eeg_readings['gamma'] = np.random.normal(size=100)

        self.alphaPlot = self.pw.plot(title="B", y=self.eeg_readings['alpha'], pen=(0, 255, 0, 100))
        self.betaPlot  = self.pw.plot(title="B", y=self.eeg_readings['beta'],  pen=(255, 10, 0, 255))
        self.gammaPlot = self.pw.plot(title="B", y=self.eeg_readings['delta'], pen=(100, 100, 255, 100))
        self.deltaPlot = self.pw.plot(title="B", y=self.eeg_readings['gamma'], pen=(255, 255, 100, 100))

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
