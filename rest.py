from flask import Flask, jsonify

app = Flask(__name__)


def serve():
    app.run(port=26548, debug=True)


@app.route('/test')
def get_test():
    return jsonify(['this', 42, 'nice', 3.14])
