import json
from unittest.mock import patch
import pytest

from requests import codes

from models import Post

mock_create_post_body = {"body": "Hello, world!"}
mock_post_id = 1


@pytest.fixture()
def mock_find_post_by_id():
    mock_post = Post()
    mock_post.id = mock_post_id

    with patch(
        "blueprints.posts.Post.find_post_by_id", return_value=mock_post
    ):
        yield


@pytest.fixture()
def mock_set_post_id():
    def mock_set_post_id(post):
        post.id = mock_post_id

    with patch(
        "blueprints.posts.db.session.add", side_effect=mock_set_post_id
    ), patch("blueprints.posts.db.session.commit"):

        yield


def test_get_post_happy_path(mock_client, mock_find_post_by_id):
    response = mock_client.get("/post/{0}".format(mock_post_id))
    assert response.status_code == codes.ok

    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["id"] == mock_post_id


def test_get_post_not_found(mock_client):
    with patch("blueprints.posts.Post.find_post_by_id", return_value=None):
        response = mock_client.get("/post/{0}".format(mock_post_id))
        assert response.status_code == codes.not_found


def test_delete_post(mock_client, mock_find_post_by_id):
    with patch("blueprints.posts.db.session.delete"), patch(
        "blueprints.posts.db.session.commit"
    ):
        response = mock_client.delete("/post/{0}".format(mock_post_id))
        assert response.status_code == codes.ok


def test_create_post(mock_client, mock_set_post_id):
    response = mock_client.post(
        "/posts",
        data=json.dumps(mock_create_post_body),
        content_type="application/json",
    )
    assert response.status_code == codes.created

    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["id"] == mock_post_id


def test_update_post(mock_client, mock_find_post_by_id, mock_set_post_id):
    response = mock_client.put(
        "/post/{0}".format(mock_post_id),
        data=json.dumps(mock_create_post_body),
        content_type="application/json",
    )
    assert response.status_code == codes.ok

    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["body"] == mock_create_post_body["body"]
