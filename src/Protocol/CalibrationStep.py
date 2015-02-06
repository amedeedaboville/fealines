from Step import Step
import random
from os import system
import subprocess
from pyqtgraph.Qt import QtCore, QtGui


class CalibrationStep(Step):
    """
    A calibration step which asks users to list members of categories.
    This is similar to the one in the Calm app.
    """
    def __init__(self, props):
        super(CalibrationStep, self).__init__(props)
        self.word_count = 0

        with open('protocols/dictionary.txt') as f:
            self.words = f.read().splitlines()
        self.say_timer = QtCore.QTimer()

    def startStep(self, callback):
        self.callback = callback
        self.timer_widget.start()
        self.horseshoe.start()

        self.say_instructions()
        self.say_timer.singleShot(1 * 7000, self.next_word)
        return self.widget

    def endStep(self):
        super(Step, self).endStep()
        self.thread.quit()

    def say_instructions(self):
        instructions = "When you hear each category, try to think of as many things that belong in that category"
        self.say_string(instructions)

    def say_word(self):
        word = random.choice(self.words)
        self.say_string(word)

    def next_word(self):
        if self.word_count < 5:
            self.word_count += 1
            self.say_word()
            self.say_timer.singleShot(2 * 1000, self.next_word)
        else:
            print "calibration almost over"
            self.say_timer.singleShot(5 * 1000, self.endStep)

    def say_string(self, string):
        subprocess.Popen(["say", string])
        # system(u'say "{0:s}"'.format(string))
