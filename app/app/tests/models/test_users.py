import pytest

from models import db, User
from tests import create_test_app


@pytest.fixture
def mock_db():
    test_app = create_test_app(db_uri="sqlite:///../test.db")
    with test_app.app_context():
        db.init_app(test_app)

        yield db


def test_find_user(mock_db):
    found_user = User.find_user("", "")
    assert found_user is None
