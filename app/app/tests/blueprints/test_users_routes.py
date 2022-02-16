import json
from unittest.mock import patch

import bcrypt
from requests import codes

from models import User

mock_username = "username"
mock_password = "password"
mock_create_user_body = {"username": mock_username, "password": mock_password}
mock_user_id = 1


def test_create_user(mock_client):
    with patch("blueprints.users.db.session.add") as mock_add, patch(
        "blueprints.users.db.session.commit"
    ):

        def mock_add_side_effect(user):
            user.id = mock_user_id

        mock_add.side_effect = mock_add_side_effect

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


def test_get_user_authorized(mock_client):
    with patch("blueprints.users.db.session.add") as mock_add, patch(
        "blueprints.users.db.session.commit"
    ), patch(
        "blueprints.users.User.find_user_by_username"
    ) as mock_find_user_by_username:

        def mock_add_side_effect(user):
            user.id = mock_user_id

        mock_add.side_effect = mock_add_side_effect

        response = mock_client.post(
            "/users",
            data=json.dumps(mock_create_user_body),
            content_type="application/json",
        )
        assert response.status_code == codes.created

        response_body = json.loads(response.get_data(as_text=True))

        found_user = User()
        found_user.id = mock_user_id
        found_user.username = mock_username
        mock_find_user_by_username.return_value = found_user

        response = mock_client.get(
            "/user",
            headers={
                "Authorization": "Bearer {0}".format(
                    response_body["access_token"]
                )
            },
        )
        assert response.status_code == codes.found


def test_login_happypath(mock_client):
    with patch(
        "blueprints.users.User.find_user_matching_password"
    ) as find_user_matching_password, patch(
        "blueprints.users.User.find_user_by_username"
    ) as mock_find_user_by_username:
        found_user = User()
        found_user.id = mock_user_id
        found_user.username = mock_username
        found_user.set_password(mock_password)
        find_user_matching_password.return_value = found_user

        response = mock_client.post(
            "/login",
            data=json.dumps(mock_create_user_body),
            content_type="application/json",
        )
        assert response.status_code == codes.ok

        response_body = json.loads(response.get_data(as_text=True))

        mock_find_user_by_username.return_value = found_user

        response = mock_client.get(
            "/user",
            headers={
                "Authorization": "Bearer {0}".format(
                    response_body["access_token"]
                )
            },
        )
        assert response.status_code == codes.found
