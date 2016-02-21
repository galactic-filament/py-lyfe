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


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(32))

    def as_dict(self):
        return {'id': self.id, 'body': self.body}


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
    post = Post()
    post.body = request.json['body']
    db.session.add(post)
    db.session.commit()
    return jsonify(post.as_dict())


@app.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.filter_by(id=id).first()
    return jsonify(post.as_dict())


@app.route('/post/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return jsonify([])


@app.route('/post/<int:id>', methods=['PUT'])
def put_post(id):
    post = Post.query.filter_by(id=id).first()
    post.body = request.json['body']
    db.session.add(post)
    db.session.commit()
    return jsonify(post.as_dict())
