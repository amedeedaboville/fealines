import json

class Protocol:
    def __init__(self, fileName):
        with open(fileName) as contents:
            json_protocol = json.load(contents)
            self.steps = [Step(step) for step in json_protocol]
class Step:
    def __init__(self, props):
        self.record =  (props['record'] == 'true') or True
        self.connect = (props['connect'] == 'true') or True
        self.duration = props['duration'] or 10
        self.graph = props['graph'] or 'all'
