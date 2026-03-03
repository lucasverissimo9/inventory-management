import json

class Mock():
    def load_payload(path):
        with open(path, 'rt') as f:
            payload = json.load(f)
            return payload