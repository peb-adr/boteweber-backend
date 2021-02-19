from datetime import datetime

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

from src import sql, error
from src import schema

app = Flask(__name__)
CORS(app)


def serve():
    app.run(port=26548, debug=True)


# following HTTP status codes are used:
# 200 - OK
# 201 - Created
# 202 - Accepted
# 400 - Bad Request
# 404 - Not Found
# 415 - Unsupported Media Type
# 500 - Internal Server Error


#
# TEST
#


@app.route('/test', methods=['GET'])
def get_test():
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    try:
        data = sql.select('subscriber')
        for i in range(0, len(data)):
            data[i] = schema.convert_instance_formatted_properties_to_json('subscriber', data[i])
        code = 200
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/test', methods=['POST'])
def post_test():
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    data, code = validate_request_body()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('subscriber', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('subscriber', data)
        data = sql.insert('subscriber', data)
        data = schema.convert_instance_formatted_properties_to_json('subscriber', data)
        code = 201
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


#
# SUBSCRIBERS
#


@app.route('/subscribers', methods=['GET'])
def get_subscribers():
    args, code = validate_request_query(['page', 'perpage', 'idsonly'])
    if code != 202:
        return make_response(jsonify(args), code)

    page = None
    if 'page' in args:
        if 'perpage' in args:
            page = (args['page'], args['perpage'])
        else:
            page = (args['page'], 3)

    try:
        if 'idsonly' not in args:
            data = sql.select('subscriber', orderby=['name ASC', 'email ASC'], page=page)
            for i in range(0, len(data)):
                data[i] = schema.convert_instance_formatted_properties_to_json('subscriber', data[i])
        else:
            data = sql.select_ids('subscriber', orderby=['name ASC', 'email ASC'])
        code = 200
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/subscribers/<int:id>', methods=['GET'])
def get_subscribers_id(id):
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    try:
        data = sql.select_by_id('subscriber', id)
        data = schema.convert_instance_formatted_properties_to_json('subscriber', data)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/subscribers', methods=['POST'])
def post_subscribers():
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    data, code = validate_request_body()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('subscriber', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('subscriber', data)
        data = sql.insert('subscriber', data)
        data = schema.convert_instance_formatted_properties_to_json('subscriber', data)
        code = 201
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/subscribers/<int:id>', methods=['PUT'])
def put_subscribers_id(id):
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    data, code = validate_request_body()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('subscriber', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('subscriber', data)
        data = sql.update_by_id('subscriber', id, data)
        data = schema.convert_instance_formatted_properties_to_json('subscriber', data)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/subscribers/<int:id>', methods=['DELETE'])
def delete_subscribers_id(id):
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    try:
        data = sql.delete_by_id('subscriber', id)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


#
# GROUPS
#


@app.route('/groups', methods=['GET'])
def get_groups():
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    try:
        data = sql.select('group')
        for i in range(0, len(data)):
            data[i] = schema.convert_instance_formatted_properties_to_json('group', data[i])
        code = 200
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/groups/<int:id>', methods=['GET'])
def get_groups_id(id):
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    try:
        data = sql.select_by_id('group', id)
        data = schema.convert_instance_formatted_properties_to_json('group', data)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/groups', methods=['POST'])
def post_groups():
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    data, code = validate_request_body()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('group', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('group', data)
        data = sql.insert('group', data)
        data = schema.convert_instance_formatted_properties_to_json('group', data)
        code = 201
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/groups/<int:id>', methods=['PUT'])
def put_groups_id(id):
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    data, code = validate_request_body()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('group', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('group', data)
        data = sql.update_by_id('group', id, data)
        data = schema.convert_instance_formatted_properties_to_json('group', data)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/groups/<int:id>', methods=['DELETE'])
def delete_groups_id(id):
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    try:
        data = sql.delete_by_id('group', id)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


#
# NEWS
#


@app.route('/news', methods=['GET'])
def get_news():
    args, code = validate_request_query(['page', 'perpage', 'idsonly'])
    if code != 202:
        return make_response(jsonify(args), code)

    page = None
    if 'page' in args:
        if 'perpage' in args:
            page = (args['page'], args['perpage'])
        else:
            page = (args['page'], 3)
    try:
        if 'idsonly' not in args:
            data = sql.select('news', orderby=['priority DESC', 'timestamp DESC'], page=page)
            for i in range(0, len(data)):
                data[i] = schema.convert_instance_formatted_properties_to_json('news', data[i])
        else:
            data = sql.select_ids('news', orderby=['priority DESC', 'timestamp DESC'])
        code = 200
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/news/<int:id>', methods=['GET'])
def get_news_id(id):
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    try:
        data = sql.select_by_id('news', id)
        data = schema.convert_instance_formatted_properties_to_json('news', data)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/news', methods=['POST'])
def post_news():
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    data, code = validate_request_body()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('news', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('news', data)
        data = sql.insert('news', data)
        data = schema.convert_instance_formatted_properties_to_json('news', data)
        code = 201
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/news/<int:id>', methods=['PUT'])
def put_news_id(id):
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    data, code = validate_request_body()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('news', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('news', data)
        data = sql.update_by_id('news', id, data)
        data = schema.convert_instance_formatted_properties_to_json('news', data)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/news/<int:id>', methods=['DELETE'])
def delete_news_id(id):
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    try:
        data = sql.delete_by_id('news', id)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


#
# INFO
#


@app.route('/info', methods=['GET'])
def get_info():
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    try:
        data = sql.select_by_id('info', 1)
        data = schema.convert_instance_formatted_properties_to_json('info', data)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/info', methods=['PUT'])
def put_info():
    args, code = validate_request_query()
    if code != 202:
        return make_response(jsonify(args), code)
    data, code = validate_request_body()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('info', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('info', data)
        data = sql.update_by_id('info', 1, data)
        data = schema.convert_instance_formatted_properties_to_json('info', data)
        code = 200
    except error.NotFoundError as e:
        data = make_error_data(e)
        code = 404
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


def resolve_relations(data, schema_name):
    d = schema.get(schema_name)
    if not d:
        return
    pass


def validate_request_body():
    if not request.is_json:
        return make_error_data(error.BadRequestError("Request data must be JSON")), 415
    data = request.get_json(silent=True)
    if not data:
        return make_error_data(error.BadRequestError("JSON data corrupt")), 400
    return data, 202


def validate_request_query(accepted_params=None):
    if accepted_params is None:
        accepted_params = []

    args = dict()
    for k, v in request.args.items():
        try:
            if k not in accepted_params:
                raise error.BadRequestError("Query parameter " + k + " is not accepted by this route")

            if k == 'page':
                args['page'] = int(v)
            if k == 'perpage':
                if 'page' not in request.args:
                    raise error.BadRequestError("Query parameter perpage requires query parameter page")
                args['perpage'] = int(v)
            if k == 'search':
                args['search'] = v
            if k == 'idsonly':
                if len(request.args) > 1:
                    raise error.BadRequestError("Query parameter idsonly is incompatible with other query parameters")
                args['idsonly'] = True
        except KeyError:
            return make_error_data(error.BadRequestError("Query parameter " + k + " not recognized")), 400
        except ValueError:
            return make_error_data(error.BadRequestError("Query parameter " + k + " must be an integer")), 400
        except error.BadRequestError as e:
            return make_error_data(e), 400
    return args, 202


def make_error_data(e):
    return {'error': e.message}
