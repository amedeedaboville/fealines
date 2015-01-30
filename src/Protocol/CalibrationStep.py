from Step import Step
import random
from os import system
from pyqtgraph.Qt import QtCore, QtGui


class CalibrationStep(Step):
    """
    A calibration step which asks users to list members of categories.
    This is similar to the one in the Calm app.
    """
    def __init__(self, props):
        super(CalibrationStep, self).__init__(props)
        with open('protocols/dictionary.txt') as f:
            self.words = f.read().splitlines()
        self.say_timer = QtCore.QTimer()

        self.word_count = 0
        self.say_instructions()

        self.say_timer.singleShot(1 * 1000, self.next_word)


    def say_instructions(self):
        instructions = "When you hear each category, try to think of as many things that belong in that category"
        system("say '%s'" % instructions)

    def say_word(self):
        word = random.choice(self.words)
        system("say '%s'" % word)

    def next_word(self):
        if self.word_count < 5:
            self.word_count += 1
            self.say_word()
            self.say_timer.singleShot(2 * 1000, self.next_word)
        else:
            print "calibration almost over"
            self.say_timer.singleShot(5 * 1000, self.endStep)

