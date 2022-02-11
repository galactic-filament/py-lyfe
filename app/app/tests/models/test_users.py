from uuid import uuid4

from models import User

mock_username = uuid4()
mock_password = "password"


def test_find_user_not_found(mock_db):
    found_user = User.find_user_matching_password("", "")
    assert found_user is None


def test_find_user_happy_path(mock_db):
    new_user = User()
    new_user.username = mock_username
    new_user.set_password(mock_password)
    mock_db.session.add(new_user)
    mock_db.session.commit()

    found_user = User.find_user_matching_password(mock_username, mock_password)
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
