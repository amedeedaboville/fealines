from Step import Step
from pyqtgraph.Qt import QtGui, QtCore
import muselo


class ConnectionStep(Step):
    """
    A calibration step which asks users to list members of categories.
    This is similar to the one in the Calm app.
    """
    def __init__(self, props):
        super(ConnectionStep, self).__init__(props)
        # self.say_timer = QtCore.QTimer()

        self.time_to_finish = 10
        self.f_widget = QtGui.QWidget()
        self.f_layout = QtGui.QVBoxLayout()
        self.progress_bars = [QtGui.QProgressBar() for _ in range(4)]
        self.timers = [QtCore.QElapsedTimer() for _ in range(4)]

        for timer in self.timers:
            timer.invalidate()
        for bar in self.progress_bars:
            bar.setMinimum(0)
            bar.setMaximum(self.time_to_finish)
            self.f_layout.addWidget(bar)

        self.f_widget.setLayout(self.f_layout)
        self.grid.addWidget(self.f_widget)

        muselo.server.register_listener('/muse/elements/horseshoe', self.receive_horseshoe)

    def receive_horseshoe(self, path, args):
        good = 0
        for idx, (conn, timer) in enumerate(zip(args, self.timers)):
            print conn, idx
            if conn == 1 or idx == 3: #good
                if not timer.isValid():
                    timer.start()
                else:
                    print "Timer is still good, elapsed: %f" % (timer.elapsed() / 1e3)
                    if timer.elapsed() / 1e3 > self.time_to_finish:
                        good += 1
            else:
                timer.invalidate()
        for bar, timer in zip(self.progress_bars, self.timers):
            if timer.isValid():
                bar.setValue(timer.elapsed() / 1e3)
            else:
                bar.setValue(0)
        if good == 4:
            self.done()

    # def paintEvent(self, QPaintEvent):
    #     qp = QtGui.QPainter()
    #     qp.begin(self)
    #     height = 30
    #     width  = 100
    #
    #     current_x = 100
    #     current_y = 100
    #     color = QtGui.QColor(0, 0, 0)
    #     color.setNamedColor('#d4d4d4')
    #     qp.setPen(color)
    #     for i in range(5):
    #         qp.drawRect(current_x, current_y, width, height)
    #         current_y += 50
    #     qp.end()
