import bcrypt
from flask import Blueprint, jsonify, request
from requests import codes

from models import db, User

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/users", methods=["POST"])
def posts():
    user = User()
    user.username = request.json["username"]
    user.password = bcrypt.hashpw(
        request.json["password"].encode(), bcrypt.gensalt()
    ).decode()
    db.session.add(user)
    db.session.commit()

    return jsonify(user.as_dict()), codes.created
