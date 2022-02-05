import os

from app import create_app

app = create_app(os.environ["DATABASE_HOST"], os.environ["APP_LOG_DIR"])

app.debug = True
app.run(host="0.0.0.0", port=int(os.environ["APP_PORT"]))
