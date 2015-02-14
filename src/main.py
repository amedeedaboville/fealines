import signal
import json
import os.path

from PyQt4.QtGui import QMainWindow, QAction, QLabel, QApplication
from PyQt4.QtCore import QVariant
from muselo import *
from Protocol.feaProtocol import Protocol, ProtocolNotLoaded

signal.signal(signal.SIGINT, signal.SIG_DFL)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.open_config()
        self.num_recent_pcl = 5
        self.initUI()

    def open_config(self):
        cfg_filename = 'config.json'
        if os.path.exists(cfg_filename):
            self.config = json.load(open(cfg_filename))
        else:
            self.config = {}
        print self.config

        recent_key = "recent_protocols"
        self.config.setdefault(recent_key, [])
        self.recent_pcl_filenames = self.config[recent_key]
        self.recent_pcls = []
        for pcl_filename in self.recent_pcl_filenames:
            with open(pcl_filename) as pcl_file:
                pcl = json.load(pcl_file)
                pcl.setdefault("name", "Unnamed Protocol")
                pcl.setdefault("description", "This protocol doesn't have a description.")
                self.recent_pcls.append({
                    "name": pcl['name'],
                    "description": pcl['description'],
                    "filename": pcl_filename
                })

    def open_recent_pcl(self):
        action = self.sender()
        if action:
            filename = str(action.data().toString())
            self.executeProtocol(filename)

    def initUI(self):
        closeAction = QAction('Close', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Application')
        closeAction.triggered.connect(lambda: sys.exit(0))

        loadAction = QAction('Load Protocol', self)
        loadAction.setStatusTip('Load the Default Protocol')
        loadAction.triggered.connect(self.executeProtocol)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(closeAction)
        load_menu = menubar.addMenu('&Load')
        load_menu.addAction(loadAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(closeAction)
        self.toolbar.addAction(loadAction)

        load_menu.addSeparator()
        for idx, recent_pcl in enumerate(self.recent_pcls):
            print recent_pcl['name']
            new_action = QAction("%d %s" % (idx + 1, recent_pcl['name']), self)
            new_action.triggered.connect(self.open_recent_pcl)
            new_action.setData(QVariant(recent_pcl['filename']))
            load_menu.addAction(new_action)

        self.setGeometry(1000,1000,1000,1000)
        self.setWindowTitle('fealines')
        self.setCentralWidget(QLabel("No protocol running"))
        self.show()


    def executeProtocol(self, filename="./protocols/graph_only.json"):
        print u"loading protocol {0:s}".format(filename)
        try:
            self.pcl = Protocol(filename, self.protocolEnded)
        except ProtocolNotLoaded:
            print "protocol not loaded..."
        self.central_widget = self.pcl.main_widget
        self.setCentralWidget(self.central_widget)
        self.pcl.start()

    def protocolEnded(self):
        self.setCentralWidget(QLabel("No protocol loaded"))


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()
    sys.exit(0)

if __name__ == '__main__':
    main()
