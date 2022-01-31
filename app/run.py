import os

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Dao

dao = Dao(SQLAlchemy())

app = create_app(os.environ["DATABASE_HOST"], dao, os.environ["APP_LOG_DIR"])

app.debug = True
app.run(host="0.0.0.0", port=int(os.environ["APP_PORT"]))
