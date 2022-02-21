import os
import traceback
from uuid import uuid4

import pytest
from flask import Flask
from werkzeug.exceptions import HTTPException

import blueprints
import forms
import models
from models import User


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

    yield app


@pytest.fixture(scope="session")
def mock_client(mock_app):
    with mock_app.app_context():
        models.init_app(mock_app, "")
        blueprints.register_blueprints(mock_app, "SECRET")
        forms.init_app(mock_app, "SECRET")

        yield mock_app.test_client()


@pytest.fixture(scope="session")
def mock_db(mock_app):
    dir_path = os.path.dirname(__file__)

    with mock_app.app_context():
        models.init_app(
            mock_app, "sqlite:///{0}/../../test.db".format(dir_path)
        )

        yield models.db


mock_username = "username"
mock_password = "password"
mock_login_request_body = {
    "username": mock_username,
    "password": mock_password,
}
mock_user_id = 1


@pytest.fixture()
def mock_user():
    user = User()
    user.id = mock_user_id
    user.username = mock_username
    user.set_password(mock_password)

    yield user


@pytest.fixture()
def mock_unique_user_id():
    yield str(uuid4())
