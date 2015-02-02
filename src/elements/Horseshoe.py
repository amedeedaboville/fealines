from PyQt4.QtCore import pyqtSignal
from pyqtgraph.Qt import QtCore, QtGui
import muselo


class HorseshoeWidget(QtGui.QWidget):

    trigger = pyqtSignal()

    def __init__(self):
        super(HorseshoeWidget, self).__init__()
        self.horseshoe = [0, 0, 0, 0]
        self.forehead = 0
        self.layout = QtGui.QHBoxLayout()
        self.labels = []
        self.colors = []

        self.trigger.connect(self.update_labels)
        self.load_pixmaps()

        for idx in self.horseshoe:
            new_label = QtGui.QLabel()
            self.labels.append(new_label)
            self.layout.addWidget(new_label)
        self.setLayout(self.layout)

        self.setStyleSheet("background-image: ./img/horseshoe/horseshoe.png")

        # self.setGeometry(300, 300, 350, 100)
        self.resize(300, 300)
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
        for idx in range(4):
            for desc in descs:
                filename = "./img/horseshoe/%s-%s.png" % (idx, desc)
                self.qimages[desc].append(QtGui.QImage())
                self.qimages[desc][idx].load(filename)
                self.pixmaps[desc].append(QtGui.QPixmap.fromImage(self.qimages[desc][idx]))


    def receive_horseshoe(self, path, args):
        print "horseshoe"
        print path, args
        self.horseshoe = [int(arg) for arg in args]
        self.trigger.emit()

    def receive_forehead(self, path, args):
        print 'forehead'
        self.forehead = int(args[0])
        self.trigger.emit()

    def update_labels(self):
        print "labels"
        for idx,number in enumerate(self.horseshoe):
            if number == 1:
                desc = 'good'
                self.labels[idx].setPixmap(self.pixmaps[desc][idx])
            elif number == 2:
                desc = 'ok'
                self.labels[idx].setPixmap(self.pixmaps[desc][idx])
            else:
                desc = 'bad'
                # self.labels[idx].setPixmap(None)
                self.labels[idx].setPixmap(self.pixmaps['good'][idx])
            print idx, number, desc
