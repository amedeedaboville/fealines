from Protocol.feaProtocol import *
class TestProtocol:

    # def setup(self):
    #     self.protocol = Protocol()

    def test_load(self):
       protocol = Protocol('./protocols/record.json')
       assert len(protocol.steps) == 1
       step = protocol.steps[0]
       assert step.record == True
       assert step.connect == True
       # assert(step.graph == ) Unsure how to specify this for now
       assert(step.duration is not None) #Implement time lengths later
