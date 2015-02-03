import random
from PyQt4.QtCore import pyqtSignal
from pyqtgraph.Qt import QtCore, QtGui
import muselo


class HorseshoeWidget(QtGui.QLabel):

    trigger = pyqtSignal()

    def __init__(self):
        super(HorseshoeWidget, self).__init__()
        self.horseshoe = [0, 0, 0, 0]
        self.forehead = 0
        self.layout = QtGui.QGridLayout()
        self.labels = [0] * 5
        self.colors = []

        self.trigger.connect(self.update_labels)
        self.load_pixmaps()
        self.update_labels()

        # self.labels = [ QtGui.QLabel() for idx in self.horseshoe]
        # The row/columns are:
        # 1 | fore  |2
        # 0 |    |3
        # self.layout.addWidget(self.labels[0], 1, 0)
        # self.layout.addWidget(self.labels[1], 0, 0)
        # self.layout.addWidget(self.labels[2], 0, 3)
        # self.layout.addWidget(self.labels[3], 1, 3)
        # self.setLayout(self.layout)

        self.setStyleSheet("""HorseshoeWidget {
        border-image:  url('./img/horseshoe/horseshoe.png');
        background-repeat: no-repeat; }""")

        # self.setGeometry(300, 300, 350, 100)
        self.setFixedSize(84, 84)

        self.show()

    def start(self):
        muselo.server.register_listener('/muse/elements/horseshoe', self.receive_horseshoe)
        muselo.server.register_listener('/muse/elements/touching_forehead', self.receive_forehead)

    def stop(self):
        muselo.server.remove_listener('/muse/elements/horseshoe', self.receive_horseshoe)
        muselo.server.remove_listener('/muse/elements/touching_forehead', self.receive_forehead)

    def load_pixmaps(self):
        descs = ['good', 'ok', 'bad']
        self.pixmaps = {'good':[], 'ok':[], 'bad':[]}
        self.qimages = {'good':[], 'ok':[], 'bad':[]}
        for idx in range(5):
            for desc in descs:
                filename = "./img/horseshoe/%d-%s.png" % (idx, desc)
                self.qimages[desc].append(QtGui.QImage())
                self.qimages[desc][idx].load(filename)
                self.pixmaps[desc].append(QtGui.QPixmap.fromImage(self.qimages[desc][idx]))


    def receive_horseshoe(self, path, args):
        print path, args
        self.horseshoe = [int(arg) for arg in args]
        self.trigger.emit()

    def receive_forehead(self, path, args):
        print "receiving forehead"
        self.forehead = int(args[0])
        self.trigger.emit()

    def read_description(self, number):
        if number == 1:
            desc = 'good'
        elif number == 2:
            desc = 'ok'
        else:
            desc = 'bad'
        return desc

    def update_labels(self):
        print "labels"
        for idx, number in enumerate(self.horseshoe + [self.forehead]):
            desc = self.read_description(number)
            desc = random.choice(['bad', 'ok', 'good']) #for debugging
            print idx, desc
            self.labels[idx] = self.pixmaps[desc][idx]
        self.repaint()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        for img in self.labels:
            qp.drawPixmap(0, 0, 84, 84, img)
        qp.end()
