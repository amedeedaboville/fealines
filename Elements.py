
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
    def read_signal(sig):
        bands = ['alpha', 'beta', 'gamma', 'delta', 'theta']
        locations = ['0', '1', '2', '3']
        all = bands * locations
        if  sig is "all":
            return all
