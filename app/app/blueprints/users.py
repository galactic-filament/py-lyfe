from flask import Blueprint, jsonify, request
from requests import codes
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

from models import db, User

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/users", methods=["POST"])
def create_user():
    user = User()
    user.username = request.json["username"]
    user.set_password(request.json["password"])
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.username)

    return (
        jsonify({"user": user.as_dict(), "access_token": access_token}),
        codes.created,
    )


@users_blueprint.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    found_user = User.find_user_by_username(get_jwt_identity())
    if found_user is None:
        return jsonify({}), codes.not_found

    return jsonify({"user": found_user.as_dict()}), codes.found
