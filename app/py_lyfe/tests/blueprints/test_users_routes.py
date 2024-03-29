import json
from unittest.mock import patch

import bcrypt
import pytest
from requests import codes

from py_lyfe.models import User, Comment, Role
from py_lyfe.tests.conftest import mock_username, mock_password, mock_user_id

mock_create_user_body = {"username": mock_username, "password": mock_password}


@pytest.fixture()
def mock_find_user_matching_password(mock_user):
    with patch(
        "blueprints.users.User.find_user_matching_password",
        return_value=mock_user,
    ) as patch_find_user_matching_password:
        yield patch_find_user_matching_password


@pytest.fixture()
def mock_find_user_by_username(mock_user):
    with patch(
        "blueprints.users.User.find_user_by_username", return_value=mock_user
    ) as patch_find_user_by_username:
        yield patch_find_user_by_username


@pytest.fixture()
def mock_set_user_id():
    def mock_set_user_id(user):
        user.id = mock_user_id

    with patch(
        "blueprints.users.db.session.add", side_effect=mock_set_user_id
    ), patch("blueprints.users.db.session.commit"):

        yield


def test_create_user(mock_client, mock_set_user_id):
    response = mock_client.post(
        "/users",
        data=json.dumps(mock_create_user_body),
        content_type="application/json",
    )
    assert response.status_code == codes.created

    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["user"]["id"] == mock_user_id
    assert bcrypt.checkpw(
        mock_create_user_body["password"].encode(),
        response_body["user"]["hashed_password"].encode(),
    )


def test_get_user_unauthorized(mock_client):
    response = mock_client.get("/user")
    assert response.status_code == codes.unauthorized


def test_get_user_authorized(
    mock_client, mock_set_user_id, mock_find_user_by_username
):
    response = mock_client.post(
        "/users",
        data=json.dumps(mock_create_user_body),
        content_type="application/json",
    )
    assert response.status_code == codes.created
    response_body = json.loads(response.get_data(as_text=True))

    response = mock_client.get(
        "/user",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.found


def test_login_happy_path(
    mock_client, mock_find_user_matching_password, mock_find_user_by_username
):
    response = mock_client.post(
        "/login",
        data=json.dumps(mock_create_user_body),
        content_type="application/json",
    )
    assert response.status_code == codes.ok
    response_body = json.loads(response.get_data(as_text=True))

    response = mock_client.get(
        "/user",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.found


def test_login_invalid(mock_client, mock_find_user_matching_password):
    mock_find_user_matching_password.return_value = None
    response = mock_client.post(
        "/login",
        data=json.dumps(mock_create_user_body),
        content_type="application/json",
    )
    assert response.status_code == codes.bad_request


def test_login_admin_happy_path(
    mock_client, mock_find_user_matching_password, mock_find_user_by_username
):
    response = mock_client.post(
        "/login",
        data=json.dumps(mock_create_user_body),
        content_type="application/json",
    )
    assert response.status_code == codes.ok
    response_body = json.loads(response.get_data(as_text=True))

    user = User()
    role = Role()
    role.name = "admin"
    user.user_roles.append(role)
    mock_find_user_by_username.return_value = user

    response = mock_client.get(
        "/user/admin",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.ok


def test_login_admin_unauth(
    mock_client, mock_find_user_matching_password, mock_find_user_by_username
):
    response = mock_client.post(
        "/login",
        data=json.dumps(mock_create_user_body),
        content_type="application/json",
    )
    assert response.status_code == codes.ok
    response_body = json.loads(response.get_data(as_text=True))

    response = mock_client.get(
        "/user/admin",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.unauthorized


def test_user_comments(
    mock_client, mock_find_user_matching_password, mock_find_user_by_username
):
    response = mock_client.post(
        "/login",
        data=json.dumps(mock_create_user_body),
        content_type="application/json",
    )
    assert response.status_code == codes.ok
    response_body = json.loads(response.get_data(as_text=True))

    user = User()
    user.comments.append(Comment())
    mock_find_user_by_username.return_value = user

    response = mock_client.get(
        "/user/comments",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.ok

    response_body = json.loads(response.get_data(as_text=True))
    assert len(response_body["comments"]) == 1
