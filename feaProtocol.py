import json
from Elements import EEGPlot, TimerWidget
from pyqtgraph import QtGui


class Protocol:
    def __init__(self, fileName):
        with open(fileName) as contents:
            json_protocol = json.load(contents)
            self.steps = [Step(step) for step in json_protocol]


class Step:
    def __init__(self, props):
        self.record = (props['record'] == 'true') or True
        self.connect = (props['connect'] == 'true') or True
        if props['duration'] is not None:
            times = [int(x) for x in props['duration'].split(":")]
            self.duration = times[0]*3600 + times[1]*60 + times[2]
        else:
            self.duration = 600

        self.graph = props['graph'] or 'all'

    def renderWidget(self):
        grid = QtGui.QGridLayout()
        if self.graph is not None:
            self.plot = EEGPlot(self.graph)

        self.timer = TimerWidget(self.duration, self.endStep)
        grid.addWidget(self.timer, 1, 1)
        grid.addWidget(self.plot, 1, 2)

        return grid

    def endStep(self):
        print "step over"
