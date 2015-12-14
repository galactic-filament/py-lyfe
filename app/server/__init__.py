from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

host = 'db'
if os.environ['ENV'] == 'travis':
    host = 'localhost'
uri = 'postgres://postgres@{0}/postgres'.format(host)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(120))

    def __init__(self, body):
        self.body = body


@app.route('/')
def home():
    return 'Hello, world!'


@app.route('/ping')
def ping():
    return 'Pong'


@app.route('/reflection', methods=['POST'])
def reflection():
    return jsonify(request.json)


@app.route('/posts', methods=['POST'])
def posts():
    post = Posts(request.json['body'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'id': post.id})
