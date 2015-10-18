from flask import Flask, jsonify, request
from app import arithmetic
import functools

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/receive-json', methods=['POST'])
def receive_json():
    return jsonify(request.get_json())


@app.route('/add', methods=['POST'])
def add():
    payload = request.get_json()
    sum = functools.reduce(arithmetic.add, payload['numbers'])
    return jsonify({'sum': sum})
