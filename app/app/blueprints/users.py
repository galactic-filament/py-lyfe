from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, current_user
from requests import codes

from models import db, User

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/users", methods=["POST"])
def create_user():
    user = User()
    user.username = request.json["username"]
    user.set_password(request.json["password"])
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user)

    return (
        jsonify({"user": user.as_dict(), "access_token": access_token}),
        codes.created,
    )


@users_blueprint.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    return (
        jsonify(
            {
                "user": current_user.as_dict(),
                "comments": [x.as_dict() for x in current_user.comments],
            }
        ),
        codes.found,
    )
