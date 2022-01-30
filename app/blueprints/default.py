from flask import Blueprint, jsonify, request
from requests import codes

default_blueprint = Blueprint('default', __name__)


@default_blueprint.route('/')
def home():
    return 'Hello, world!', codes.ok, {'Content-type': 'text/plain'}


@default_blueprint.route('/ping')
def ping():
    return 'Pong', codes.ok, {'Content-type': 'text/plain'}


@default_blueprint.route('/reflection', methods=['POST'])
def reflection():
    return jsonify(request.json)
