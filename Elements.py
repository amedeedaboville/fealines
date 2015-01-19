
class EEGPlot:
    def __init__(self):
        self.eeg_readings['alpha'] = np.random.normal(size=100)
        self.eeg_readings['beta']  = np.random.normal(size=100)
        self.eeg_readings['delta'] = np.random.normal(size=100)
        self.eeg_readings['gamma'] = np.random.normal(size=100)

        self.alphaPlot = self.pw.plot(title="B", y=self.eeg_readings['alpha'], pen=(0, 255, 0, 100))
        self.betaPlot  = self.pw.plot(title="B", y=self.eeg_readings['beta'],  pen=(255, 10, 0, 255))
        self.gammaPlot = self.pw.plot(title="B", y=self.eeg_readings['delta'], pen=(100, 100, 255, 100))
        self.deltaPlot = self.pw.plot(title="B", y=self.eeg_readings['gamma'], pen=(255, 255, 100, 100))

class