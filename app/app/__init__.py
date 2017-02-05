from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
import logging
import json
from pythonjsonlogger import jsonlogger
from app import default, posts

# flask init
app = Flask(__name__)

# flask logging
if os.environ.get('REQUEST_LOGGING'):
    log_handler = logging.FileHandler('/var/log/app.log')
    log_handler.setFormatter(jsonlogger.JsonFormatter())
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)
    @app.before_request
    def log_request():
        body = '' if not request.json else json.dumps(request.json)

        app.logger.info('Url hit', extra={
            'contentType': request.headers['content-type'],
            'method': request.method,
            'url': request.path,
            'body': body
        })

# db init
uri = 'postgres://postgres@{0}/postgres'.format(os.environ['DATABASE_HOST'])
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# blueprints
app.register_blueprint(default.default_blueprint)
app.register_blueprint(posts.get_blueprint(db))
