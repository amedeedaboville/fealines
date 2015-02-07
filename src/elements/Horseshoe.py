from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QGridLayout, QLabel, QImage, QPixmap, QPainter
import muselo


class HorseshoeWidget(QLabel):

    trigger = pyqtSignal()

    def __init__(self, parent):
        super(HorseshoeWidget, self).__init__(parent)
        self.horseshoe = [0, 0, 0, 0]
        self.forehead = 0
        self.layout = QGridLayout()
        self.labels = [0] * 5
        self.colors = []

        self.trigger.connect(self.update_labels)
        self.load_pixmaps()
        self.update_labels()

        self.setStyleSheet("""HorseshoeWidget {
        border-image:  url('./img/horseshoe/horseshoe.png');
        background-repeat: no-repeat; }""")

        self.setFixedSize(84, 84)
        print "about to show"
        self.show()

    def start(self):
        print "starting horseshoe"
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
                self.qimages[desc].append(QImage())
                self.qimages[desc][idx].load(filename)
                self.pixmaps[desc].append(QPixmap.fromImage(self.qimages[desc][idx]))

    def receive_horseshoe(self, path, args):
        self.horseshoe = [int(arg) for arg in args]
        self.trigger.emit()

    def receive_forehead(self, path, args):
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
        for idx, number in enumerate(self.horseshoe + [self.forehead]):
            desc = self.read_description(number)
            # desc = random.choice(['bad', 'ok', 'good']) #for debugging
            self.labels[idx] = self.pixmaps[desc][idx]
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        for img in self.labels:
            qp.drawPixmap(0, 0, 84, 84, img)
        qp.end()