import json
import logging

from flask import Flask, request
from pythonjsonlogger import jsonlogger

from blueprints import posts
from blueprints.default import default_blueprint


def create_app(db_host, dao, app_log_dir):
    app = Flask(__name__)

    # db init
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres@{0}/postgres".format(
        db_host
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    dao.init_app(app)

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
    log_handler = logging.FileHandler("{0}/app.log".format(app_log_dir))
    log_handler.setFormatter(jsonlogger.JsonFormatter())
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)

    # blueprints
    app.register_blueprint(default_blueprint)
    app.register_blueprint(posts.get_blueprint(dao))

    return app
