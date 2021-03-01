from os import listdir

from src import schema


def main():
    queries = {
        'queries': [],
        'queries_drop': [],
        'queries_relation': [],
        'queries_relation_drop': []
    }

    for filename in listdir('schema'):
        if filename.endswith('.json'):
            query_create_table(queries, filename[:-5])

    return '\n'.join(queries['queries_relation_drop'] +
                     queries['queries_drop'] +
                     queries['queries'] +
                     queries['queries_relation'])


def query_create_table(queries, schema_name):
    d = schema.get(schema_name)
    if not d:
        return

    s = "CREATE TABLE " + d['title'] + " (id INT NOT NULL AUTO_INCREMENT, "
    for p in d['required']:
        # if prop contains other ids => create relation table
        if d['properties'][p]['type'] == 'array':
            query_create_relation_table(queries, d['title'], p)
        else:
            s += p + " " + sql_type(d['properties'][p]) + " NOT NULL, "
    s += "PRIMARY KEY (id));"

    queries['queries_drop'].append("DROP TABLE IF EXISTS " + d['title'] + ";")
    queries['queries'].append(s)


def query_create_relation_table(queries, from_table, to_table):
    s = "CREATE TABLE " + from_table + "_" + to_table + "("
    s += "id INT NOT NULL AUTO_INCREMENT, "
    s += from_table + "_id INT NOT NULL, "
    s += to_table + "_id INT NOT NULL, "
    s += "PRIMARY KEY (id), "
    s += "FOREIGN KEY (" + from_table + "_id) REFERENCES " + from_table + "(id), "
    s += "FOREIGN KEY (" + to_table + "_id) REFERENCES " + to_table + "(id)"
    s += ");"

    queries['queries_relation_drop'].append("DROP TABLE IF EXISTS " + from_table + "_" + to_table + ";")
    queries['queries_relation'].append(s)


def sql_type(json_prop):
    try:
        if 'format' in json_prop:
            return {
                'date-time': 'DATETIME'
            }[json_prop['format']]
        return {
            'array': 'JSON',
            'boolean': 'BOOL',
            'integer': 'INT',
            'null': 'INT',
            'number': 'FLOAT',
            'object': 'JSON',
            'string': 'TEXT'
        }[json_prop['type']]
    except KeyError:
        return 'TEXT'


if __name__ == '__main__':
    print(main())
