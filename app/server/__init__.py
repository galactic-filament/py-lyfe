from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/receive-json', methods=['POST'])
def receive_json():
    return jsonify(request.get_json())
