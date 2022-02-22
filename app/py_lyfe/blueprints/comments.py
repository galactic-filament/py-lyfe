from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from requests import codes

from py_lyfe.models import Comment, db

comments_blueprint = Blueprint("comments", __name__)


@comments_blueprint.route("/comments", methods=["POST"])
@jwt_required()
def create_comment():
    comment = Comment()
    comment.body = request.json["body"]
    current_user.comments.append(comment)
    db.session.add(current_user)
    db.session.commit()

    return (
        jsonify({"comments": [x.as_dict() for x in current_user.comments]}),
        codes.created,
    )


@comments_blueprint.route("/comments", methods=["GET"])
@jwt_required()
def get_comments():
    return (
        jsonify({"comments": [x.as_dict() for x in current_user.comments]}),
        codes.ok,
    )


@comments_blueprint.route("/comment/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update_comment(comment_id):
    comment = Comment.find_comment_by_id(comment_id)
    if comment is None:
        return jsonify({}), codes.not_found

    if comment.user_id != current_user.id:
        return jsonify({}), codes.unauthorized

    comment.body = request.json["body"]
    db.session.add(comment)
    db.session.commit()

    return jsonify({"comment": comment.as_dict()}), codes.ok


@comments_blueprint.route("/comment/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    comment = Comment.find_comment_by_id(comment_id)
    if comment is None:
        return jsonify({}), codes.not_found

    if comment.user_id != current_user.id:
        return jsonify({}), codes.unauthorized

    db.session.remove(comment)
    db.session.commit()

    return jsonify({}), codes.ok
