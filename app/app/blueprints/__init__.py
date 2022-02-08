from flask_jwt_extended import JWTManager

from blueprints.default import default_blueprint
from blueprints.posts import posts_blueprint
from blueprints.users import users_blueprint


def register_blueprints(app, jwt_secret_key):
    app.config["JWT_SECRET_KEY"] = jwt_secret_key
    JWTManager(app)

    app.register_blueprint(default_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(users_blueprint)
