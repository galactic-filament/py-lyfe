from flask import Blueprint, jsonify, request

posts_blueprint = Blueprint('posts', __name__)


def get_blueprint(db):
    class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        body = db.Column(db.String(32))

        def as_dict(self):
            return {'id': self.id, 'body': self.body}

    @posts_blueprint.route('/posts', methods=['POST'])
    def posts():
        post = Post()
        post.body = request.json['body']
        db.session.add(post)
        db.session.commit()
        return jsonify(post.as_dict())

    @posts_blueprint.route('/post/<int:id>', methods=['GET'])
    def get_post(id):
        post = Post.query.filter_by(id=id).first()
        return jsonify(post.as_dict())

    @posts_blueprint.route('/post/<int:id>', methods=['DELETE'])
    def delete_post(id):
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        return jsonify([])

    @posts_blueprint.route('/post/<int:id>', methods=['PUT'])
    def put_post(id):
        post = Post.query.filter_by(id=id).first()
        post.body = request.json['body']
        db.session.add(post)
        db.session.commit()
        return jsonify(post.as_dict())

    return posts_blueprint
