from elements.EEGPlot import EEGPlot
from elements.TimerWidget import TimerWidget
from elements.Horseshoe import HorseshoeWidget

from PyQt4.QtCore import QObject
from PyQt4.QtGui import QWidget, QHBoxLayout, QPushButton

class Step(QObject):
    def __init__(self, params):
        super(Step, self).__init__()
        self.parse_properties(params)
        self.initUI()
        print "Step {0} initialized".format(self.name)

        self.data_dict = {"name": self.name}

    def parse_properties(self, props):
        self.data_widgets = {}
        props.setdefault('name', "")
        props.setdefault('duration', "")
        props.setdefault('next_button', "true")
        props.setdefault('show_timer', "true")
        props.setdefault('record', "true")

        self.name = props['name']
        self.record = props['record']
        self.show_timer = (props['show_timer'] == 'true')
        self.duration = self.parse_duration(props['duration'])
        self.has_next_button = (props['next_button'] == 'true')

        if 'graph' in props:
            self.graph = True
            plot_params = props['graph']
            self.plot = EEGPlot(plot_params)
            self.data_widgets['plot'] = self.plot
        else:
            self.graph = False


    def initUI(self):
        self.widget = QWidget()
        self.grid = QHBoxLayout()

        if self.duration:
            self.timer_widget = TimerWidget(self.duration, self.endStep)
            if self.show_timer:
                self.grid.addWidget(self.timer_widget)
        if self.graph:
            self.grid.addWidget(self.plot.pw)
            self.horseshoe = HorseshoeWidget(self.plot.pw)
        else:
            self.horseshoe = HorseshoeWidget(self.widget)
        self.widget.setLayout(self.grid)


    def startStep(self, callback):
        print "starting a step"
        if self.duration:
            self.timer_widget.start()
        self.horseshoe.start()
        if self.graph:
            self.plot.start()
        self.callback = callback

    def endStep(self):
        for i in range(self.grid.count()): self.grid.itemAt(i).widget().close()  # clear the layout
        if self.graph:
            self.plot.stop()
        if self.record:
            for name, widget in self.data_widgets.iteritems():
                self.data_dict[name] = widget.serialize()
        if self.has_next_button:
            self.next_button = QPushButton()
            self.next_button.setText("Press to Continue")
            self.next_button.clicked.connect(lambda: self.callback(self.data_dict))
            self.grid.addWidget(self.next_button)
        else:
            self.callback(self.data_dict)

    def parse_duration(self, time_string):
        if len(time_string) == 0:
            return None
        else:
            times = [int(x) for x in time_string.split(":")]
            times.reverse()  # Now we have ss:mm:hh:dd
            multipliers = [1, 60, 3600, 3600*24]
            time_in_secs = sum([unit* multiplier for unit, multiplier in zip(times, multipliers)])
            return time_in_secs
