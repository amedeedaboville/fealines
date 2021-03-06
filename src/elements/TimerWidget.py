from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QTimer
class TimerWidget(QLabel):
    def __init__(self, time, callback):
        """
        :param time:
        The duration of the countdown timer, in seconds
        :param callback:
        The callback for when the timer finishes
        """
        super(TimerWidget, self).__init__()

        self.setText("%d:%02d" % (time / 60., time % 60))

        self.callback = callback
        self.time_left = time

        self.total_timer = QTimer(self)
        self.total_timer.setSingleShot(True)
        self.total_timer.timeout.connect(self.stop)

        self.seconds_timer = QTimer(self)
        self.seconds_timer.timeout.connect(self.updateDisplay)

    def start(self):
        self.total_timer.start(self.time_left * 1000)
        self.seconds_timer.start(1000)

    def stop(self):
        self.updateDisplay(0)
        self.seconds_timer.stop()
        self.callback()

    def updateDisplay(self,new_time=None):
        if new_time is None:
            self.time_left -= 1
            new_time = self.time_left
        self.setText("%d:%02d" % (new_time / 60., new_time % 60))
