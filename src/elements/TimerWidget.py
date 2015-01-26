from pyqtgraph.Qt import QtCore, QtGui
class TimerWidget(QtGui.QLabel):
    def __init__(self, time, callback):
        """
        :param time:
        The duration of the countdown timer, in seconds
        :param callback:
        The callback for when the timer finishes
        """
        super(TimerWidget, self).__init__()

        self.setText("%d:%02d" % (time / 60., time % 60))

        self.time_left = time
        self.total_timer = QtCore.QTimer(self)
        self.total_timer.timeout.connect(callback)

        self.seconds_timer = QtCore.QTimer(self)
        self.seconds_timer.timeout.connect(self.updateDisplay)

    def start(self):
        self.total_timer.start(self.time_left * 1000)
        self.seconds_timer.start(1000)

    def updateDisplay(self):
        self.time_left -= 1
        self.setText("%d:%02d" % (self.time_left / 60., self.time_left % 60))

