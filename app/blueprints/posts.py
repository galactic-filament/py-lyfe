from flask import Blueprint, jsonify, request
from requests import codes

from models.post import Post

posts_blueprint = Blueprint("posts", __name__)


def get_blueprint(dao):
    @posts_blueprint.route("/posts", methods=["POST"])
    def posts():
        post = Post()
        post.body = request.json["body"]
        dao.add(post)

        return jsonify(post.as_dict()), codes.created

    @posts_blueprint.route("/post/<int:id>", methods=["GET"])
    def get_post(post_id):
        post = Post.query.filter_by(id=post_id).first()

        return jsonify(post.as_dict())

    @posts_blueprint.route("/post/<int:id>", methods=["DELETE"])
    def delete_post(post_id):
        post = Post.query.filter_by(id=post_id).first()
        dao.delete(post)

        return jsonify([])

    @posts_blueprint.route("/post/<int:id>", methods=["PUT"])
    def put_post(post_id):
        post = Post.query.filter_by(id=post_id).first()
        post.body = request.json["body"]
        dao.add(post)

        return jsonify(post.as_dict())

    return posts_blueprint
