import json

class feaProtocol:
    def __init__(self):
       pass

    def loadFromFile(self, fileName):
        json_file = json.loads(fileName)
        for step in json_file:
            print step
