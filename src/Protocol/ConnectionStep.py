from Step import Step
import random
from os import system
from pyqtgraph.Qt import QtCore, QtGui


class ConnectionStep(Step):
    """
    A calibration step which asks users to list members of categories.
    This is similar to the one in the Calm app.
    """
    def __init__(self, props):
        super(ConnectionStep, self).__init__(props)
        # self.say_timer = QtCore.QTimer()
        self.fwidget = FillWidget()
        self.grid.addWidget(self.fwidget)
        print "fwidget initialized"

class FillWidget(QtGui.QWidget):
    def __init__(self):
        super(FillWidget, self).__init__()

    def paintEvent(self, QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)

        self.draw_bg_rects(qp)
        # color = QtGui.QColor(0, 0, 0)
        # color.setNamedColor('#d4d4d4')
        # qp.setPen(color)
        #
        # qp.setBrush(QtGui.QColor(200, 0, 0))
        # qp.drawRect(10, 15, 90, 60)
        #
        # qp.setBrush(QtGui.QColor(255, 80, 0, 160))
        # qp.drawRect(130, 15, 90, 60)
        #
        # qp.setBrush(QtGui.QColor(25, 0, 90, 200))
        # qp.drawRect(250, 15, 90, 60)

        qp.end()


    def draw_bg_rects(self, qp):
        height = 30
        width  = 100
        current_x = 100
        current_y = 100
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)
        for i in range(5):
            qp.drawRect(current_x, current_y, width, height)
            current_y += 50
