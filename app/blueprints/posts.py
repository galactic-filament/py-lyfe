from flask import Blueprint, jsonify, request
from requests import codes

from models import db
from models.post import Post, find_post_by_id

posts_blueprint = Blueprint("posts", __name__)


def get_blueprint():
    @posts_blueprint.route("/posts", methods=["POST"])
    def posts():
        post = Post()
        post.body = request.json["body"]
        db.session.add(post)
        db.session.commit()

        return jsonify(post.as_dict()), codes.created

    @posts_blueprint.route("/post/<int:post_id>", methods=["GET"])
    def get_post(post_id):
        post = find_post_by_id(post_id)

        return jsonify(post.as_dict())

    @posts_blueprint.route("/post/<int:post_id>", methods=["DELETE"])
    def delete_post(post_id):
        post = find_post_by_id(post_id)
        db.session.delete(post)
        db.session.commit()

        return jsonify([])

    @posts_blueprint.route("/post/<int:post_id>", methods=["PUT"])
    def put_post(post_id):
        post = Post.query.filter_by(id=post_id).first()
        post.body = request.json["body"]
        db.session.add(post)
        db.session.commit()

        return jsonify(post.as_dict())

    return posts_blueprint
