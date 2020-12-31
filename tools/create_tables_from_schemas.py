from src import schema


TABLES = [
    {
        'name': 'info',
        'schema': 'info'
    },
    {
        'name': 'news',
        'schema': 'neu'
    }
]


def main():
    table_queries = list()

    for t in TABLES:
        table_queries.append("DROP TABLE IF EXISTS " + t['name'] + ";")
        s = "CREATE TABLE " + t['name'] + " (id INT NOT NULL AUTO_INCREMENT, "
        d = schema.get(t['schema'], path_prefix='..')
        for p in d['required']:
            s += p + " " + sql_type(d['properties'][p]['type']) + " NOT NULL, "
        s += "PRIMARY KEY (id));"
        table_queries.append(s)

    return '\n'.join(table_queries)


def sql_type(json_type):
    return {
        'array': 'JSON',
        'boolean': 'BOOL',
        'integer': 'INT',
        'null': 'INT',
        'number': 'FLOAT',
        'object': 'JSON',
        'string': 'TEXT'
    }[json_type]


if __name__ == '__main__':
    print(main())
