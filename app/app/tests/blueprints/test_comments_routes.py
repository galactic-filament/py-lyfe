import json
from unittest.mock import patch

import pytest
from requests import codes

from tests.conftest import mock_login_request_body
from models import User, Comment

mock_create_comment_request_body = {"body": "Hello, world!"}
mock_comment_id = 1


@pytest.fixture()
def mock_find_user_matching_password(mock_user):
    with patch(
        "blueprints.users.User.find_user_matching_password",
        return_value=mock_user,
    ):
        yield


@pytest.fixture()
def mock_find_user_by_username(mock_user):
    with patch(
        "blueprints.users.User.find_user_by_username", return_value=mock_user
    ) as patch_find_user_by_username:
        yield patch_find_user_by_username


@pytest.fixture()
def mock_set_comment_id():
    def mock_set_comment_id(comment):
        comment.id = mock_comment_id

    with patch(
        "blueprints.users.db.session.add", side_effect=mock_set_comment_id
    ), patch("blueprints.users.db.session.commit"):

        yield


def test_create_comment(
    mock_client,
    mock_find_user_matching_password,
    mock_find_user_by_username,
    mock_set_comment_id,
):
    response = mock_client.post(
        "/login",
        data=json.dumps(mock_login_request_body),
        content_type="application/json",
    )
    assert response.status_code == codes.ok
    response_body = json.loads(response.get_data(as_text=True))

    user = User()
    comment = Comment()
    comment.user = user
    comment.id = None
    comment.body = mock_create_comment_request_body["body"]
    user.comments.append(comment)
    mock_find_user_by_username.return_value = user

    response = mock_client.post(
        "/comments",
        data=json.dumps(mock_create_comment_request_body),
        content_type="application/json",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.created

    mock_create_comment_request_body.update({"id": None})

    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["comments"][0] == mock_create_comment_request_body
