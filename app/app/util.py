import json
import logging
from logging import FileHandler

from flask import Flask, request
from pythonjsonlogger import jsonlogger

import blueprints
import models


def create_app(db_uri, app_log_dir):
    app = Flask(__name__)

    # misc init
    models.init_app(app, db_uri)
    blueprints.register_blueprints(app, "wew lad")

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

    return app
