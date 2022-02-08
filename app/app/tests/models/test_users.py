from uuid import uuid4

import pytest

from models import db, User
from tests import create_test_app

test_username_prefix = uuid4()


@pytest.fixture
def mock_db():
    test_app = create_test_app(db_uri="sqlite:///../test.db")
    with test_app.app_context():
        db.init_app(test_app)

        yield db


mock_username = "{0}_{1}".format(test_username_prefix, uuid4())
mock_password = "password"


def test_find_user_not_found(mock_db):
    found_user = User.find_user("", "")
    assert found_user is None


def test_find_user_happy_path(mock_db):
    new_user = User()
    new_user.username = mock_username
    new_user.set_password(mock_password)
    mock_db.session.add(new_user)
    mock_db.session.commit()

    found_user = User.find_user(mock_username, mock_password)
    assert found_user is not None


def test_clear_test_users(mock_db):
    test_prefix = str(uuid4())

    new_user = User()
    new_user.username = "{0}_user".format(test_prefix)
    new_user.set_password(mock_password)
    mock_db.session.add(new_user)
    mock_db.session.commit()

    total_deleted = User.clear_test_users(test_prefix)
    assert total_deleted == 1
