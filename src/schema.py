import json


def get(name):
    with open('schema/' + name + '.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data
