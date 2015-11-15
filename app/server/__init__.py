from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, world!'


@app.route('/ping')
def ping():
    return 'Pong'


@app.route('/reflection', methods=['POST'])
def reflection():
    return jsonify(request.json)
