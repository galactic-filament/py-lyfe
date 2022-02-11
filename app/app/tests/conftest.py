import os

import pytest
from flask import Flask

import blueprints
import models


@pytest.fixture(scope="session")
def mock_client():
    app = Flask(__name__)

    with app.app_context():
        models.init_app(app, "")
        blueprints.register_blueprints(app, "settings.JWT_SECRET")

        return app.test_client()


@pytest.fixture
def mock_db():
    dir_path = os.path.dirname(__file__)

    app = Flask(__name__)

    with app.app_context():
        models.init_app(app, "sqlite:///{0}/../../test.db".format(dir_path))

        yield models.db
