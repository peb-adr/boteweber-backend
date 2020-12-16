import json

from src import sql, rest


def main():
    with open('sql_conn_config.json', 'r') as f:
        conn_config = json.loads(f.read())
        f.close()
    if type(conn_config) != dict:
        conn_config = {}

    sql.init(conn_config)
    rest.serve()


if __name__ == '__main__':
    main()
