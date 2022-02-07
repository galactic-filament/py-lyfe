import os

from util import create_app

app = create_app(os.environ["DATABASE_URI"], os.environ["APP_LOG_DIR"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ["APP_PORT"]))
