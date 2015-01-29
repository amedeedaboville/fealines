import json
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
        with open("./recordings/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"), "w+") as file:
            json.dump(self.session, file)
        print self.session

    def end_step(self, data_dict):
        self.session['steps'].append({})
        self.session['steps'][self.current_step_idx]['end'] = datetime.datetime.now()
        self.session['steps'][self.current_step_idx]['data'] = data_dict
        self.next_step()

    def next_step(self):
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


