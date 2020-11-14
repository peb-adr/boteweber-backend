from datetime import datetime

from flask import Flask, jsonify, request

import error
import sql

app = Flask(__name__)


def serve():
    app.run(port=26548, debug=True)


# @app.route('/test', methods=['GET'])
# def get_test():
#     return jsonify(['this', 42, 'nice', 3.14])


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
        return data, code

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
        return data, code

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


def validate_request():
    if not request.is_json:
        return {}, 415
    data = request.get_json(silent=True)
    if not data:
        return {}, 400
    if not isinstance(data, dict):
        return {}, 400
    if 'title' not in data or 'message' not in data:
        return {}, 400
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now()
    return data, 202
