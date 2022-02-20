from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, current_user
from requests import codes

from blueprints.decorators import role_required
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


@users_blueprint.route("/login", methods=["POST"])
def login():
    user = User.find_user_matching_password(
        request.json["username"], request.json["password"]
    )
    if user is None:
        return jsonify({}), codes.bad_request

    access_token = create_access_token(identity=user)

    return (
        jsonify({"user": user.as_dict(), "access_token": access_token}),
        codes.ok,
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


@users_blueprint.route("/user/admin", methods=["GET"])
@role_required("admin")
@jwt_required()
def get_admin_info():
    return jsonify({}), codes.ok


@users_blueprint.route("/user/comments", methods=["GET"])
@jwt_required()
def get_user_comments():
    return (
        jsonify({"comments": [x.as_dict() for x in current_user.comments]}),
        codes.ok,
    )
