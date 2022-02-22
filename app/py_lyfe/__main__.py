import json
import logging
from logging import FileHandler

from flask import Flask, request
from pythonjsonlogger import jsonlogger

from py_lyfe import blueprints, models, settings

app = Flask(__name__)


# misc init
models.init_app(app, settings.DATABASE_URI)
blueprints.register_blueprints(app, settings.JWT_SECRET)

# request logging init
log_handler = FileHandler("{0}/app.log".format(settings.APP_LOG_DIR))
log_handler.setFormatter(jsonlogger.JsonFormatter())
app.logger.setLevel(logging.INFO)
app.logger.addHandler(log_handler)


# request logging callback
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(settings.APP_PORT))
