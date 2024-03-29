from flask_jwt_extended import JWTManager

from py_lyfe.blueprints.comments import comments_blueprint
from py_lyfe.blueprints.default import default_blueprint
from py_lyfe.blueprints.posts import posts_blueprint
from py_lyfe.blueprints.users import users_blueprint
from py_lyfe.models import User


def register_blueprints(app, jwt_secret_key):
    app.config["JWT_SECRET_KEY"] = jwt_secret_key
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.username

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]

        return User.find_user_by_username(identity)

    app.register_blueprint(default_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(comments_blueprint)
