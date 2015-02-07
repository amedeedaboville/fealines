from Step import Step
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
import muselo


class ConnectionStep(Step):
    """
    A connection step which waits for all sensors to have good signal for 10 seconds.
    """
    update_bars_signal = pyqtSignal()
    end_connection_signal = pyqtSignal()

    def __init__(self, props):
        super(ConnectionStep, self).__init__(props)

        self.time_to_finish = 10
        self.f_widget = QtGui.QWidget()
        self.f_layout = QtGui.QVBoxLayout()
        self.progress_bars = [QtGui.QProgressBar() for _ in range(4)]
        self.timers = [QtCore.QElapsedTimer() for _ in range(4)]

        for timer in self.timers:
            timer.invalidate()

        self.title_label = QtGui.QLabel("Adjust the Headband until all of the bars are full")
        self.title_label.setMaximumHeight(100)
        self.f_layout.addWidget(self.title_label)
        self.colors = ["#ea6a1f", "#009986", "#555c99", "#d20e8a"]
        for bar, color in zip(self.progress_bars, self.colors):
            bar.setMinimum(0)
            bar.setMaximum(self.time_to_finish)
            bar.setTextVisible(False)
            bar.setStyleSheet((u' QProgressBar::chunk {{ background: {0:s}; }}' +
                               u' QProgressBar {{border: 1px solid gray}}').format(color));

            self.f_layout.addWidget(bar)

        self.update_bars_signal.connect(self.update_bars)
        self.end_connection_signal.connect(self.end_connection)

        self.f_widget.setLayout(self.f_layout)
        self.grid.addWidget(self.f_widget)

        muselo.server.register_listener('/muse/elements/horseshoe', self.receive_horseshoe)

    def receive_horseshoe(self, path, args):
        good = 0
        for idx, (conn, timer) in enumerate(zip(args, self.timers)):
            print conn, idx
            if conn == 1:
                if not timer.isValid():
                    timer.start()
                else:
                    print "Timer is still good, elapsed: %f" % (timer.elapsed() / 1e3)
                    if timer.elapsed() / 1e3 > self.time_to_finish:
                        good += 1
            else:
                timer.invalidate()
        self.update_bars.emit()
        if good == 4:
            self.end_connection.emit()

    def update_bars(self):
        for bar, timer in zip(self.progress_bars, self.timers):
            if timer.isValid():
                bar.setValue(timer.elapsed() / 1e3)
            else:
                bar.setValue(0)

    def end_connection(self):
        muselo.server.remove_listener('/muse/elements/horseshoe', self.receive_horseshoe)
        self.f_widget.close()
        self.grid.removeWidget(self.f_widget)
        self.next_button = QtGui.QPushButton()
        self.next_button.setText("Press Here to Continue")
        self.next_button.clicked.connect(self.endStep)
        self.grid.addWidget(self.next_button)

