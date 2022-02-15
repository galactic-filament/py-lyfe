import os
import traceback

import pytest
from flask import Flask
from werkzeug.exceptions import HTTPException

import blueprints
import models


@pytest.fixture(scope="session")
def mock_app():
    app = Flask(__name__)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return e

    @app.errorhandler(Exception)
    def handle_exception(e):
        print("received exception, printing traceback")
        print(traceback.format_exc())
        print("done printing traceback")

        if isinstance(e, HTTPException):
            return e

    return app


@pytest.fixture(scope="session")
def mock_client(mock_app):
    with mock_app.app_context():
        models.init_app(mock_app, "")
        blueprints.register_blueprints(mock_app, "settings.JWT_SECRET")

        return mock_app.test_client()


@pytest.fixture(scope="session")
def mock_db(mock_app):
    dir_path = os.path.dirname(__file__)

    with mock_app.app_context():
        models.init_app(
            mock_app, "sqlite:///{0}/../../test.db".format(dir_path)
        )

        yield models.db
