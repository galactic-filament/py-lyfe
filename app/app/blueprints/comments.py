from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from requests import codes

from models import db, Comment

comments_blueprint = Blueprint("comments", __name__)


@comments_blueprint.route("/comments", methods=["POST"])
@jwt_required()
def posts():
    comment = Comment()
    comment.body = request.json["body"]
    current_user.comments.append(comment)
    db.session.add(current_user)
    db.session.commit()

    return (
        jsonify({"comments": [x.as_dict() for x in current_user.comments]}),
        codes.created,
    )
