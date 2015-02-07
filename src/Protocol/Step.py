from elements.EEGPlot import EEGPlot
from elements.TimerWidget import TimerWidget
from elements.Horseshoe import HorseshoeWidget
from pyqtgraph import QtGui, QtCore


class Step(QtCore.QObject):
    def __init__(self, props):
        super(Step, self).__init__()
        self.parse_properties(props)
        self.initUI()

        self.data_dict = {"name": self.name}

    def parse_properties(self, props):
        self.data_widgets = {}
        self.record = ('record' in props and props['record'] == 'true')
        self.name = props['name'] if 'name' in props else ''

        self.graph = ('graph' in props and props['graph'] != 'false')
        if self.graph:
            self.plot = EEGPlot(props['graph'])
            self.data_widgets['plot'] = self.plot

        if 'duration' in props:
            times = [int(x) for x in props['duration'].split(":")]
            self.duration = times[0]*3600 + times[1]*60 + times[2] #TODO: breaks on less than 2 ':'s
        else: self.duration = None

        if 'show_timer' in props:
            self.show_timer = (props['show_timer'] == 'true')
        else:
            self.show_timer = True

        if 'next_button' in props:
            self.has_next_button = (props['next_button'] == 'true')
        else:
            self.show_timer = True

    def initUI(self):
        self.widget = QtGui.QWidget()
        self.grid = QtGui.QHBoxLayout()

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
        if self.duration:
            self.timer_widget.start()
        self.horseshoe.start()
        if self.graph:
            self.plot.start()
        self.callback = callback
        return self.widget

    def endStep(self):
        if self.graph:
            self.plot.stop()
        if self.record:
            for name, widget in self.data_widgets.iteritems():
                self.data_dict[name] = widget.serialize()
        if self.has_next_button:
            self.grid.removeWidget(self.widget)
            self.next_button = QtGui.QPushButton()
            self.next_button.setText("Press to Continue")
            self.next_button.clicked.connect(self.endStep)
            self.grid.addWidget(self.next_button)
            self.next_button.clicked.connect(lambda: self.callback(self.data_dict))
        else:
            self.callback(self.data_dict)

