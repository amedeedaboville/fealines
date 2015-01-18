import feaProtocol
class TestProtocol:

    def setup(self):
        self.protocol = feaProtocol()

    def test_load(self):
       self.protocol.loadFromFile('protocols/record.json')
       assert len(self.protocol.steps) == 1
       step = self.protocol.steps[0]
       assert step.record == True
       assert step.connect == True
       # assert(step.graph == ) Unsure how to specify this for now
       assert(step.duration is not None) #Implement time lengths later
