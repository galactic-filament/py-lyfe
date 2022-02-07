import json
import logging
from logging import FileHandler

from flask import Flask, request
from pythonjsonlogger import jsonlogger

from blueprints.default import default_blueprint
from blueprints.posts import posts_blueprint
from blueprints.users import users_blueprint
from models import db


def create_app(db_uri, app_log_dir):
    app = Flask(__name__)

    # db init
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # request logging
    @app.before_request
    def log_request():
        body = "" if not request.json else json.dumps(request.json)
        content_type = (
            ""
            if not ("content-type" in request.headers)
            else request.headers["content-type"]
        )

        app.logger.info(
            "Url hit",
            extra={
                "contentType": content_type,
                "method": request.method,
                "url": request.path,
                "body": body,
            },
        )

    # flask logging
    log_handler = FileHandler("{0}/app.log".format(app_log_dir))
    log_handler.setFormatter(jsonlogger.JsonFormatter())
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)

    # blueprints
    app.register_blueprint(default_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(users_blueprint)

    return app
