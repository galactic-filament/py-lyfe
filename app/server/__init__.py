# imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

# flask init
app = Flask(__name__)

# db init
host = 'db'
if os.environ['ENV'] == 'travis':
    host = 'localhost'
uri = 'postgres://postgres@{0}/postgres'.format(host)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

# blueprints init
from app.server.posts import posts_blueprint
app.register_blueprint(posts_blueprint)


# misc route init
@app.route('/')
def home():
    return 'Hello, world!'


@app.route('/ping')
def ping():
    return 'Pong'


@app.route('/reflection', methods=['POST'])
def reflection():
    return jsonify(request.json)
