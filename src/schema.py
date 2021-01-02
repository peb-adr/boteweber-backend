from datetime import datetime
from json import load

from dateutil import parser
from jsonschema import draft7_format_checker
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import best_match
from jsonschema.validators import validator_for

from src import error


def get(name):
    with open('schema/' + name + '.json', 'r') as f:
        data = load(f)
        f.close()
    return data


def validate(name, instance):
    schema = get(name)

    # validate schema
    cls = validator_for(schema)
    try:
        cls.check_schema(schema)
    except SchemaError as e:
        raise error.ValidationError(e.message)

    # validate instance
    validator = cls(schema, format_checker=draft7_format_checker)
    e = best_match(validator.iter_errors(instance))
    if e is not None:
        raise error.ValidationError(e.message)


def convert_instance_formatted_properties_from_json(name, instance):
    schema = get(name)

    for k, v in schema['properties'].items():
        if k in instance and 'format' in v:
            # convert known formats
            if v['format'] == 'date-time':
                # instance[k] = datetime.fromisoformat(instance[k])
                instance[k] = parser.isoparse(instance[k])

    return instance


def convert_instance_formatted_properties_to_json(name, instance):
    schema = get(name)

    for k, v in schema['properties'].items():
        if k in instance and 'format' in v:
            # convert known formats
            if v['format'] == 'date-time':
                instance[k] = instance[k].isoformat() + ('Z' if not instance[k].tzinfo else '')

    return instance
