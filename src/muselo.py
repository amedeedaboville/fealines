from liblo import *
import sys
import time

class MuseServer(ServerThread):
    def __init__(self):
        ServerThread.__init__(self, 5000)
        self.listeners = {}

    def receive_signal(self, path, args):
        if path in self.listeners:
            for listener in self.listeners[path]:
                listener(path, args)
        l_ear, l_forehead, r_forehead, r_ear = args
        print "%s %f %f %f %f" % (path, l_ear, l_forehead, r_forehead, r_ear)

    def register_listener(self, signal, listener):
        if signal not in self.listeners:
            self.add_method(signal, 'ffff', self.receive_signal)
            self.listeners[signal] = []
        if listener not in self.listeners[signal]:
            self.listeners[signal].append(listener)

    def remove_listener(self, signal, listener):
        if listener in self.listeners[signal]:
            self.listeners[signal].remove(listener)

    ##handle unexpected messages
    #@make_method(None, None)
    #def fallback(self, path, args, types, src):
    #    print "Unknown message \
    #    \n\t Source: '%s' \
    #    \n\t Address: '%s' \
    #    \n\t Types: '%s ' \
    #    \n\t Payload: '%s'" \
    #    % (src.url, path, types, args)

try:
    server = MuseServer()
except ServerError, err:
    print str(err)
    sys.exit()
server.start()

if __name__ == "__main__":
    while 1:
        time.sleep(1)
