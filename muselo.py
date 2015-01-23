from liblo import *
import sys
import time

class MuseServer(ServerThread):
    def __init__(self):
        ServerThread.__init__(self, 5000)
        self.listeners = {}

    def register_listener(self, signal, listener):
        if signal not in self.listeners:
            self.listeners[signal] = []
        if listener not in self.listeners[signal]:
            self.listeners[signal].append(listener)
        print "listeners now"
        print self.listeners

    def remove_listener(self, signal, listener):
        if listener in self.listeners[signal]:
            self.listeners[signal].remove(listener)

    #receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        print "eeg received with path"
        print path
        if path in self.listeners:
            for listener in self.listeners[path]:
                listener(path, args)
        l_ear, l_forehead, r_forehead, r_ear = args
        print "%s %f %f %f %f" % (path, l_ear, l_forehead, r_forehead, r_ear)

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
