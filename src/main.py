import json

from src import sql, rest

if __name__ == '__main__':
    with open('sql_conn_config.json', 'r') as f:
        conn_config = json.loads(f.read())
        f.close()
    if type(conn_config) != dict:
        conn_config = {}

    sql.init(conn_config)
    rest.serve()
