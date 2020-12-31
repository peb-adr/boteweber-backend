import json


def get(name, path_prefix='.'):
    data = {}
    with open(path_prefix + '/schema/' + name + '.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data


def get_info():
    data = {}
    with open('schema/info.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data


def get_neu():
    data = {}
    with open('schema/neu.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data


def get_news():
    data = {}
    with open('schema/news.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data
