from Protocol.feaProtocol import *
class TestProtocol:

    # def setup(self):
    #     self.protocol = Protocol()

    def test_load(self):
       protocol = Protocol('./protocols/record.json', None) # TODO: test callback
       assert len(protocol.steps) == 1
       step = protocol.steps[0]
       assert step.record == True
       assert(step.duration == 60*10)
