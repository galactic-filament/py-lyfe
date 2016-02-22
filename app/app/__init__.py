from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app import default, posts

# flask init
app = Flask(__name__)

# db init
host = 'db'
if os.environ['ENV'] == 'travis':
    host = 'localhost'
uri = 'postgres://postgres@{0}/postgres'.format(host)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# blueprints
app.register_blueprint(default.default_blueprint)
app.register_blueprint(posts.get_blueprint(db))
