import json
import datetime
from PyQt4.QtGui import QWidget, QGridLayout
from Step import Step
from CalibrationStep import CalibrationStep
from ConnectionStep import ConnectionStep


class Protocol:
    def __init__(self, fileName, callback):
        with open(fileName) as contents:
            try:
                json_protocol = json.load(contents)
            except ValueError as e:
                print "Protocol file could not be loaded. It might have a typo."
                print "This is the error code the file gave us:"
                print e
                raise ProtocolNotLoaded

            self.steps = []
            for step in json_protocol:
                if 'type' in step:
                    if step['type'] == 'calibration':
                        self.steps.append(CalibrationStep(step))
                    elif step['type'] == 'connection':
                        self.steps.append(ConnectionStep(step))
                    else:
                        print u"Unknown step type '{0:s}'".format(step['type'])
                else:
                    self.steps.append(Step(step))

        self.session = {
            'num_steps': len(self.steps),
            'steps': []
        }

        self.callback = callback
        self.current_step_idx = 0
        self.current_step = self.steps[self.current_step_idx]
        self.main_widget = QWidget()
        self.layout = QGridLayout()
        self.main_widget.setLayout(self.layout)

    def start(self):
        print "starting protocol"
        self.current_step.startStep(self.end_step)
        self.current_widget  = self.current_step.widget
        self.layout.addWidget(self.current_widget)
        self.session['start'] = datetime.datetime.now()

    def end(self):
        self.session['end'] = datetime.datetime.now()
        with open("./recordings/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"), "w+") as file:
            json.dump(self.session, file, default=self.default_serializer)
        print "protocol ended. Data:"
        print self.session
        self.current_widget.close()
        self.main_widget.close()
        self.callback()

    def default_serializer(self, obj):
      if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

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
            self.current_step.startStep(self.end_step)
            self.current_widget = self.current_step.widget
            self.layout.addWidget(self.current_widget)
        else:
            self.end()


class ProtocolNotLoaded(Exception):

     def __str__(self):
         return "ProtocolNotLoaded Error"
