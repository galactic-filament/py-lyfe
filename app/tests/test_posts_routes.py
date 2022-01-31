from unittest.mock import patch

import pytest

from tests import create_post, request_json, create_test_app, MockDao


@pytest.fixture
def client():
    return create_test_app().test_client()


def test_posts(client):
    with patch.object(MockDao, "add") as mock_method:

        def side_effect(post):
            post.id = 1

        mock_method.side_effect = side_effect

        body = {"body": "Hello, world!"}
        create_post(client, body)


def test_get_post(client):
    with patch.object(MockDao, "add") as mock_method:

        def side_effect(post):
            post.id = 1

        mock_method.side_effect = side_effect

        # creating a post
        body = {"body": "Hello, world!"}
        create_response_body = create_post(client, body)

        # getting the post and asserting they match
        url = "/post/{0}".format(create_response_body["id"])
        get_response_body = request_json(client, "get", url)
        assert get_response_body["body"] == create_response_body["body"]


def test_delete_post(client):
    # creating a post
    body = {"body": "Hello, world!"}
    create_response_body = create_post(client, body)

    # deleting the post
    url = "/post/{0}".format(create_response_body["id"])
    request_json(client, "delete", url)


def test_put_post(client):
    # creating a post
    body = {"body": "Hello, world!"}
    create_response_body = create_post(client, body)

    # updating the post
    url = "/post/{0}".format(create_response_body["id"])
    body = {"body": "Jello, world!"}
    put_response_body = request_json(client, "put", url, body)
    assert body["body"] == put_response_body["body"]
