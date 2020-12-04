from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

import error
import sql

app = Flask(__name__)
CORS(app)


def serve():
    app.run(port=26548, debug=True)


@app.route('/news', methods=['GET'])
def get_news():
    try:
        data = sql.get_news()
        code = 200
    except error.DBError:
        data = []
        code = 500

    return jsonify(data), code


@app.route('/news/<int:id>', methods=['GET'])
def get_news_id(id):
    try:
        data = sql.get_news_id(id)
        code = 200
    except error.NotFoundError:
        data = {}
        code = 404
    except error.DBError:
        data = {}
        code = 500

    return jsonify(data), code


@app.route('/news', methods=['POST'])
def post_news():
    data, code = validate_request()
    if code != 202:
        return jsonify(data), code
    data = validate_news(data)

    if not data:
        return jsonify(data), 400
    try:
        data = sql.post_news(data)
        code = 201
    except error.NotFoundError:
        data = {}
        code = 404
    except error.DBError:
        data = {}
        code = 500

    return jsonify(data), code


@app.route('/news/<int:id>', methods=['PUT'])
def put_news_id(id):
    data, code = validate_request()
    if code != 202:
        return jsonify(data), code
    data = validate_news(data)
    if not data:
        return jsonify(data), 400

    try:
        data = sql.put_news_id(id, data)
        code = 200
    except error.NotFoundError:
        data = {}
        code = 404
    except error.DBError:
        data = {}
        code = 500

    return jsonify(data), code


@app.route('/news/<int:id>', methods=['DELETE'])
def delete_news_id(id):
    try:
        data = sql.delete_news_id(id)
        code = 200
    except error.NotFoundError:
        data = {}
        code = 404
    except error.DBError:
        data = {}
        code = 500

    return jsonify(data), code


@app.route('/info', methods=['GET'])
def get_info():
    try:
        data = sql.get_info_id(1)
        data = transform_info_to_json(data)
        code = 200
    except error.NotFoundError:
        data = {}
        code = 404
    except error.DBError:
        data = {}
        code = 500

    return jsonify(data), code


@app.route('/info', methods=['PUT'])
def put_info():
    data, code = validate_request()
    if code != 202:
        return jsonify(data), code
    data = validate_info(data)
    if not data:
        return jsonify(data), 400

    try:
        data = transform_info_from_json(data)
        data = sql.put_info_id(1, data)
        data = transform_info_to_json(data)
        code = 200
    except error.NotFoundError:
        data = {}
        code = 404
    except error.DBError:
        data = {}
        code = 500

    return jsonify(data), code


def validate_request():
    if not request.is_json:
        return {}, 415
    data = request.get_json(silent=True)
    if not data:
        return {}, 400
    if not isinstance(data, dict):
        return {}, 400
    return data, 202


def validate_news(data):
    if 'title' not in data or 'message' not in data:
        return {}
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now()
    return data


def validate_info(data):
    if 'text' not in data or\
            'greets' not in data or \
            'he' not in data['greets'] or \
            'top' not in data['greets']['he'] or \
            'bot' not in data['greets']['he'] or \
            'moin' not in data['greets'] or \
            'top' not in data['greets']['moin'] or \
            'bot' not in data['greets']['moin']:
        return {}
    return data


def transform_info_from_json(data):
    return {
        'text': data['text'],
        'greets_he_top': data['greets']['he']['top'],
        'greets_he_bot': data['greets']['he']['bot'],
        'greets_moin_top': data['greets']['moin']['top'],
        'greets_moin_bot': data['greets']['moin']['bot']
    }


def transform_info_to_json(data):
    return {
        'text': data['text'],
        'greets': {
            'he': {
                'top': data['greets_he_top'],
                'bot': data['greets_he_bot']
            },
            'moin': {
                'top': data['greets_moin_top'],
                'bot': data['greets_moin_bot']
            }
        }
    }
