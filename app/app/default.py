from flask import Blueprint, jsonify, request

default_blueprint = Blueprint('default', __name__)


@default_blueprint.route('/')
def home():
    return 'Hello, world!'


@default_blueprint.route('/ping')
def ping():
    return 'Pong'


@default_blueprint.route('/reflection', methods=['POST'])
def reflection():
    return jsonify(request.json)
