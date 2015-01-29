from elements.EEGPlot import EEGPlot
from elements.TimerWidget import TimerWidget
from pyqtgraph import QtGui


class Step:
    def __init__(self, props):
        self.record = (props['record'] == 'true') or True
        if props['duration'] is not None:
            times = [int(x) for x in props['duration'].split(":")]
            self.duration = times[0]*3600 + times[1]*60 + times[2]
        else:
            self.duration = 600

        self.graph = props['graph'] or 'all'
        self.name = props['name'] or ""

        self.data_dict = {"name": self.name}

        self.timer = TimerWidget(self.duration, self.endStep)

        self.widget = QtGui.QWidget()
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.timer, 1, 1)

        if self.graph is not None:
            self.plot = EEGPlot(self.graph)
            self.grid.addWidget(self.plot.pw, 1, 2)

        self.widget.setLayout(self.grid)
        self.data_widgets = {'plot': self.plot} # TODO: Add other kinds of data widgets like checkboxes

    def startStep(self, callback):
        self.timer.start()
        self.plot.start()
        self.callback = callback
        return self.widget

    def endStep(self):
        if self.graph:
            self.plot.stop()
        if self.record:
            for name, widget in self.data_widgets.iteritems():
                self.data_dict[name] = widget.serialize()
        self.callback(self.data_dict)
