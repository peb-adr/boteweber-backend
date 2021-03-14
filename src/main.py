import json

from src import sql, rest
from src import config


def main():
    init_config()

    sql.init()
    rest.serve()


def init_config():
    with open('rest_config.json', 'r') as f:
        c = json.loads(f.read())
        f.close()
    if type(c) != dict:
        c = {}
    config.rest = c

    with open('smtp_config.json', 'r') as f:
        c = json.loads(f.read())
        f.close()
    if type(c) != dict:
        c = {}
    config.smtp = c

    with open('sql_config.json', 'r') as f:
        c = json.loads(f.read())
        f.close()
    if type(c) != dict:
        c = {}
    config.sql = c


if __name__ == '__main__':
    main()
