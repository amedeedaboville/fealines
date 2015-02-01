from pyqtgraph.Qt import QtCore, QtGui
import muselo
class HorseshoeWidget(QtGui.QWidget):
    def __init__(self):
        super(HorseshoeWidget, self).__init__()
        self.horseshoe = [0, 0, 0, 0]
        self.forehead = 0
        self.layout = QtGui.QHBoxLayout()
        self.labels = []
        self.qimages = [QtGui.QImage() for x in self.horseshoe]
        self.colors = []

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
        self.pixmaps = []
        for idx in range(4):
            for desc in ['good', 'ok', 'bad']:
                filename = "./img/horseshoe/%s-%s.png" % (idx, desc)
                q = QtGui.QImage()
                self.qimages[idx].load(filename)
                self.pixmaps[idx] = QtGui.QPixmap.fromImage(qimage)
                self.pixmaps[desc][idx] = QtGui.QPixmap()


    def receive_horseshoe(self, path, args):
        print "horseshoe"
        print path, args
        if path == 'muse/elements/horseshoe/':
            self.horseshoe = [int(arg) for arg in args]
        self.update_labels()

    def receive_forehead(self, path, args):
        print 'forehead'
        if path == 'muse/elements/touching_forehead/':
            self.forehead = int(args[0])
        self.update_labels()

    def update_labels(self):
        print "labels"
        for idx,number in enumerate(self.horseshoe):
            if number == 1:
                desc = 'good'
            elif number == 2:
                desc = 'ok'
            else:
                desc = 'bad'
            self.labels[idx].setPixmap(self.pixmaps[desc][idx])
