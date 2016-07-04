from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from pythonjsonlogger import jsonlogger
from app import default, posts

# flask init
app = Flask(__name__)

# flask logging
if os.environ['REQUEST_LOGGING']:
    log_handler = logging.FileHandler('/var/log/app.log')
    log_handler.setFormatter(jsonlogger.JsonFormatter())
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)
    @app.after_request
    def log_request(response):
        app.logger.info('Url hit', extra={
            'status': response.status_code
        })
        return response

# db init
uri = 'postgres://postgres@{0}/postgres'.format(os.environ['DATABASE_HOST'])
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# blueprints
app.register_blueprint(default.default_blueprint)
app.register_blueprint(posts.get_blueprint(db))
