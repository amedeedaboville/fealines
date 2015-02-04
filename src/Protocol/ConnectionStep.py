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
        self.fwidget = FillWidget(self.endStep)
        self.grid.addWidget(self.fwidget)

class FillWidget(QtGui.QWidget):
    """
    A widget that
    """
    def __init__(self, callback):
        super(FillWidget, self).__init__()
        self.done = callback
        self.layout = QtGui.QVBoxLayout()
        self.progress_bars = [QtGui.QProgressBar() for _ in range(4)]
        self.timers = [QtCore.QElapsedTimer() for _ in range(4)]
        for bar in self.progress_bars:
            bar.setMinimum(0)
            bar.setMaximum(2000)
            self.layout.addWidget(bar)

        self.setLayout(self.layout)

        muselo.server.register_listener('/muse/elements/horseshoe', self.receive_horseshoe)

    def receive_horseshoe(self, path, args):
        good = 0
        for conn, timer in zip(args, self.timers):
            print conn
            if conn == 1 : #good
                if not timer.isValid():
                    timer.start()
                else:
                    print "Timer is still good, elapsed: %d" % (timer.elapsed())
                    if timer.elapsed() > 2000:
                        good += 1
            else:
                timer.invalidate()
        for bar, timer in zip(self.progress_bars, self.timers):
            if timer.isValid():
                bar.setValue(timer.elapsed())
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
