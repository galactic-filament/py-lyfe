# imports
from flask import Blueprint, jsonify, request

# blueprint init
default_blueprint = Blueprint('default', __name__)


# routes
@default_blueprint.route('/')
def home():
    return 'Hello, world!'


@default_blueprint.route('/ping')
def ping():
    return 'Pong'


@default_blueprint.route('/reflection', methods=['POST'])
def reflection():
    return jsonify(request.json)
