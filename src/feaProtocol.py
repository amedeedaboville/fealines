import json
from elements.EEGPlot import EEGPlot
from elements.TimerWidget import TimerWidget
import datetime
from pyqtgraph import QtGui


class Protocol:
    def __init__(self, fileName):
        with open(fileName) as contents:
            json_protocol = json.load(contents)
            self.steps = [Step(step) for step in json_protocol]

        self.session = {
            'num_steps': len(self.steps),
            'steps': []
        }

        self.current_step_idx = 0
        self.current_step = self.steps[self.current_step_idx]
        self.widget = QtGui.QWidget()

    def start(self):
        self.grid = self.current_step.startStep(self.end_step)
        self.widget.setLayout(self.grid)
        self.session['start'] = datetime.datetime.now()
        return self.widget

    def end(self):
        print "protocol ended"

    def end_step(self, data_dict):
        self.session['steps'].append({})
        self.session['steps'][self.current_step_idx]['end'] = datetime.datetime.now()
        self.session['steps'][self.current_step_idx]['data'] = data_dict
        self.next_step()

    def next_step(self):
        # self.current_step_idx += 1
        if len(self.steps) < self.current_step_idx + 1:
            self.session['steps'][self.current_step_idx]['end'] = datetime.datetime.now()
            self.current_step = self.steps[self.current_step_idx]
            # self.current_step_idx += 1
            self.grid = self.current_step.startStep(self.end_step)
            self.widget.setLayout(self.grid)
        else:
            self.end()


class Step:
    def __init__(self, props):
        self.record = (props['record'] == 'true') or True
        if props['duration'] is not None:
            times = [int(x) for x in props['duration'].split(":")]
            self.duration = times[0]*3600 + times[1]*60 + times[2]
        else:
            self.duration = 600

        self.graph = props['graph'] or 'all'

        self.timer = TimerWidget(self.duration, self.endStep)
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.timer, 1, 1)

        if self.graph is not None:
            self.plot = EEGPlot(self.graph)
            self.grid.addWidget(self.plot.pw, 1, 2)

        self.data_widgets = {'plot': self.plot} # TODO: Add other kinds of data widgets like checkboxes

    def startStep(self, callback):
        self.timer.start()
        self.plot.start()
        self.callback = callback
        return self.grid

    def endStep(self):
        self.data_dict = {}
        if self.record: #record by default
            for name, widget in self.data_widgets.iteritems():
                self.data_dict[name] = widget.serialize()
        self.callback(self.data_dict)
        print "step over"
