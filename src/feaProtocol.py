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
        self.main_widget = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()
        self.main_widget.setLayout(self.layout)

    def start(self):
        self.current_widget = self.current_step.startStep(self.end_step)
        self.layout.addWidget(self.current_widget)
        self.session['start'] = datetime.datetime.now()
        return self.main_widget

    def end(self):
        print "protocol ended. Data:"
        print self.session

    def end_step(self, data_dict):
        self.session['steps'].append({})
        self.session['steps'][self.current_step_idx]['end'] = datetime.datetime.now()
        self.session['steps'][self.current_step_idx]['data'] = data_dict
        self.next_step()

    def next_step(self):
        print "next step"
        if len(self.steps) > self.current_step_idx + 1:
            self.session['steps'][self.current_step_idx]['end'] = datetime.datetime.now()

            self.current_step_idx += 1
            self.current_step = self.steps[self.current_step_idx]
            self.current_widget.close()
            self.layout.removeWidget(self.current_widget)
            self.current_widget = self.current_step.startStep(self.end_step)
            self.layout.addWidget(self.current_widget)
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
        print "step over"
        if self.record: #record by default
            for name, widget in self.data_widgets.iteritems():
                self.data_dict[name] = widget.serialize()
        self.callback(self.data_dict)
