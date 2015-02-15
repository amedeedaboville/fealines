from Step import Step
import random
import subprocess
from PyQt4.QtCore import QTimer


class CalibrationStep(Step):
    """
    A calibration step which asks users to list members of categories.
    This is similar to the one in the Calm app.
    """
    def __init__(self, params):
        params['duration'] = '00:01:00'
        params['next_button'] = 'true'
        super(CalibrationStep, self).__init__(params)
        self.num_words = 4
        self.words_said = 0

        with open('protocols/dictionary.txt') as f:
            words = f.read().splitlines()
        self.words_to_say = random.sample(words, self.num_words)

        self.say_timer = QTimer()

    def startStep(self, callback):
        self.callback = callback
        self.horseshoe.start()

        self.say_instructions()
        self.say_timer.singleShot(1 * 7000, self.next_word)
        QTimer().singleShot(1 * 7000, self.timer_widget.start)
        return self.widget

    def say_instructions(self):
        instructions = "When you hear each category, try to think of as many things that belong in that category"
        self.say_string(instructions)

    def say_word(self):
        word = self.words_to_say[self.words_said]
        self.say_string(word)

    def next_word(self):
        if self.words_said < self.num_words:
            self.say_word()
            self.words_said += 1
            self.say_timer.singleShot(15 * 1000, self.next_word)

    def say_string(self, string):
        subprocess.Popen(["say", string])
