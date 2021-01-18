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


@app.route('/news', methods=['GET'])
def get_news():
    try:
        data = sql.select('news', ['priority DESC', 'timestamp DESC'])
        for i in range(0, len(data)):
            data[i] = schema.convert_instance_formatted_properties_to_json('neu', data[i])
        code = 200
    except error.DBError as e:
        data = make_error_data(e)
        code = 500

    return make_response(jsonify(data), code)


@app.route('/news/<int:id>', methods=['GET'])
def get_news_id(id):
    try:
        data = sql.select_by_id('news', id)
        data = schema.convert_instance_formatted_properties_to_json('neu', data)
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
    data, code = validate_request()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('neu', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('neu', data)
        data = sql.insert('news', data)
        data = schema.convert_instance_formatted_properties_to_json('neu', data)
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
    data, code = validate_request()
    if code != 202:
        return make_response(jsonify(data), code)

    try:
        schema.validate('neu', data)
    except error.ValidationError as e:
        return make_response(jsonify(make_error_data(e)), 400)

    try:
        data = schema.convert_instance_formatted_properties_from_json('neu', data)
        data = sql.update_by_id('news', id, data)
        data = schema.convert_instance_formatted_properties_to_json('neu', data)
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


@app.route('/info', methods=['GET'])
def get_info():
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
    data, code = validate_request()
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


def validate_request():
    if not request.is_json:
        return make_error_data(error.BadRequestError("Request data must be JSON")), 415
    data = request.get_json(silent=True)
    if not data:
        return make_error_data(error.BadRequestError("JSON data corrupt")), 400
    return data, 202


def make_error_data(e):
    return {'error': e.message}
