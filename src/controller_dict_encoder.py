import json


class ControllerDictEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

