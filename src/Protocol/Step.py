from elements.EEGPlot import EEGPlot
from elements.TimerWidget import TimerWidget
from elements.Horseshoe import HorseshoeWidget

from PyQt4.QtCore import QObject
from PyQt4.QtGui import QWidget, QHBoxLayout, QPushButton

class Step(QObject):
    def __init__(self, props):
        super(Step, self).__init__()
        self.parse_properties(props)
        self.initUI()
        print "Step {0} initialized".format(self.name)

        self.data_dict = {"name": self.name}

    def parse_properties(self, props):
        self.data_widgets = {}
        self.record = ('record' in props and props['record'] == 'true')
        self.name = props['name'] if 'name' in props else ''

        graph = ('graph' in props and props['graph'] != 'false')
        bar = ('bar' in props and props['bar'] != 'false')
        if graph:
            self.graph = True
            plot_params = {'bar': bar}
            self.plot = EEGPlot(plot_params, props['graph'])
        if not (graph or bar):
            self.graph = False
        elif graph and bar:
            raise Exception("Cannot have both a Bar graph and a line plot on one screen")


        if self.graph:
            plot_params = {'bar': bar}
            self.plot = EEGPlot(plot_params, props['graph'])

            self.data_widgets['plot'] = self.plot

        if 'duration' in props:
            self.duration = self.parse_duration(props['duration'])
        else:
            self.duration = None

        if 'show_timer' in props:
            self.show_timer = (props['show_timer'] == 'true')
        else:
            self.show_timer = True

        if 'next_button' in props:
            self.has_next_button = (props['next_button'] == 'true')
        else:
            self.has_next_button = True

    def initUI(self):
        self.widget = QWidget()
        self.grid = QHBoxLayout()

        if self.duration and self.show_timer:
            self.timer_widget = TimerWidget(self.duration, self.endStep)
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
        if self.graph:
            self.plot.stop()
        if self.record:
            for name, widget in self.data_widgets.iteritems():
                self.data_dict[name] = widget.serialize()
        if self.has_next_button:
            for i in range(self.grid.count()): self.grid.itemAt(i).widget().close()  # clear the layout
            self.next_button = QPushButton()
            self.next_button.setText("Press to Continue")
            self.next_button.clicked.connect(lambda: self.callback(self.data_dict))
            self.grid.addWidget(self.next_button)
        else:
            self.callback(self.data_dict)

    def parse_duration(self, time_string):
        times = [int(x) for x in time_string.split(":")]
        if len(times) > 0:
            times.reverse()  # Now we have ss:mm:hh:dd
            multipliers = [1, 60, 3600, 3600*24]
            time_in_secs = sum([unit* multiplier for unit, multiplier in zip(times, multipliers)])
            return time_in_secs
        else:
            raise ValueError("Couldn't parse step duration")