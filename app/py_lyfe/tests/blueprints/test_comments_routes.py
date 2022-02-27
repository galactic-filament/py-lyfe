import json
from unittest.mock import patch

import pytest
from requests import codes

from py_lyfe.tests.conftest import mock_login_request_body, mock_user_id
from py_lyfe.models import User, Comment

mock_create_comment_request_body = {"body": "Hello, world!", "post_id": 0}
mock_update_comment_request_body = {"body": "Jello, world!"}
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
        "blueprints.comments.db.session.add", side_effect=mock_set_comment_id
    ), patch("blueprints.comments.db.session.commit"):

        yield


@pytest.fixture()
def mock_delete_comment():
    with patch("blueprints.comments.db.session.remove"), patch(
        "blueprints.comments.db.session.commit"
    ):

        yield


@pytest.fixture()
def mock_find_comment_by_id():
    with patch(
        "blueprints.comments.Comment.find_comment_by_id",
    ) as patch_find_comment_by_id:
        yield patch_find_comment_by_id


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
    comment.post_id = mock_create_comment_request_body["post_id"]
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

    mock_create_comment_request_body.update(dict(id=None))

    response_body = json.loads(response.get_data(as_text=True))
    assert response_body == mock_create_comment_request_body


def test_get_comments(
    mock_client,
    mock_find_user_matching_password,
    mock_find_user_by_username,
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
    comment.post_id = mock_create_comment_request_body["post_id"]
    user.comments.append(comment)
    mock_find_user_by_username.return_value = user

    response = mock_client.get(
        "/comments",
        data=json.dumps(mock_create_comment_request_body),
        content_type="application/json",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.ok

    mock_create_comment_request_body.update(dict(id=None))

    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["comments"][0] == mock_create_comment_request_body


def test_update_comment_happypath(
    mock_client,
    mock_find_user_matching_password,
    mock_find_user_by_username,
    mock_find_comment_by_id,
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
    user.id = mock_user_id
    mock_find_user_by_username.return_value = user

    comment = Comment()
    comment.id = mock_comment_id
    comment.user_id = mock_user_id
    mock_find_comment_by_id.return_value = comment

    response = mock_client.put(
        "/comment/{0}".format(mock_comment_id),
        data=json.dumps(mock_update_comment_request_body),
        content_type="application/json",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.ok


def test_remove_comment_happypath(
    mock_client,
    mock_find_user_matching_password,
    mock_find_user_by_username,
    mock_find_comment_by_id,
    mock_delete_comment,
):
    response = mock_client.post(
        "/login",
        data=json.dumps(mock_login_request_body),
        content_type="application/json",
    )
    assert response.status_code == codes.ok
    response_body = json.loads(response.get_data(as_text=True))

    user = User()
    user.id = mock_user_id
    mock_find_user_by_username.return_value = user

    comment = Comment()
    comment.id = mock_comment_id
    comment.user_id = mock_user_id
    mock_find_comment_by_id.return_value = comment

    response = mock_client.delete(
        "/comment/{0}".format(mock_comment_id),
        content_type="application/json",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.ok


def test_remove_comment_unauth(
    mock_client,
    mock_find_user_matching_password,
    mock_find_user_by_username,
    mock_find_comment_by_id,
    mock_delete_comment,
):
    response = mock_client.post(
        "/login",
        data=json.dumps(mock_login_request_body),
        content_type="application/json",
    )
    assert response.status_code == codes.ok
    response_body = json.loads(response.get_data(as_text=True))

    user = User()
    user.id = mock_user_id
    mock_find_user_by_username.return_value = user

    comment = Comment()
    comment.id = mock_comment_id
    comment.user_id = -1
    mock_find_comment_by_id.return_value = comment

    response = mock_client.delete(
        "/comment/{0}".format(mock_comment_id),
        content_type="application/json",
        headers={
            "Authorization": "Bearer {0}".format(response_body["access_token"])
        },
    )
    assert response.status_code == codes.unauthorized
