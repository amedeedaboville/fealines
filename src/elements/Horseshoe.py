from pyqtgraph.Qt import QtCore, QtGui
import muselo
class HorseshoeWidget(QtGui.QWidget):
    def __init__(self):
        super(HorseshoeWidget, self).__init__()
        self.horseshoe = [0, 0, 0, 0]
        self.forehead = 0
        self.labels = [QtGui.QLabel() for img in self.horseshoe]

        # self.setGeometry(300, 300, 350, 100)
        self.resize(300, 300)
        self.show()

    def start(self):
        muselo.server.register_listener('/muse/elements/horseshoe', self.receive_horseshoe)
        muselo.server.register_listener('/muse/elements/touching_forehead', self.receive_forehead)

    def stop(self):
        muselo.server.remove_listener('/muse/elements/horseshoe', self.receive_horseshoe)
        muselo.server.remove_listener('/muse/elements/touching_forehead', self.receive_forehead)

    def receive_horseshoe(self, path, args):
        if path == 'muse/elements/horseshoe/':
            self.horseshoe = [int(arg) for arg in args]
        self.update_labels()

    def receive_forehead(self, path, args):
        if path == 'muse/elements/touching_forehead/':
            self.forehead = int(args[0])
        self.update_labels()

    def update_labels(self):
        for (label, number) in zip(self.labels, self.horseshoe):
            qimage = QtGui.QImage()
            qimage.load("./img/horseshoe/horseshoe.png")
            pixmap = QtGui.QPixmap.fromImage(qimage)
            label.setPixmaap(pixmap)
