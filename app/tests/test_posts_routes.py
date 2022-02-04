import json
from unittest.mock import patch

from requests import codes

from models.post import Post
from tests import create_test_app

mock_create_post_body = {"body": "Hello, world!"}
mock_post_id = 1


def test_get_post():
    with patch("blueprints.posts.find_post_by_id") as mock_find_post_by_id:
        mock_post = Post()
        mock_post.id = mock_post_id
        mock_find_post_by_id.return_value = mock_post

        test_client = create_test_app().test_client()
        response = test_client.get("/post/{0}".format(mock_post_id))
        assert response.status_code == codes.ok

        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"] == mock_post_id


def test_delete_post():
    with patch("blueprints.posts.find_post_by_id") as mock_find_post_by_id, patch(
        "blueprints.posts.db.session.delete"
    ) as mock_delete, patch("blueprints.posts.db.session.commit") as mock_commit:
        mock_post = Post()
        mock_post.id = mock_post_id
        mock_find_post_by_id.return_value = mock_post

        mock_delete.return_value = None
        mock_commit.return_value = None

        test_client = create_test_app().test_client()
        response = test_client.delete("/post/{0}".format(mock_post_id))
        assert response.status_code == codes.ok


def test_posts():
    with patch("blueprints.posts.db.session.add") as mock_add, patch(
        "blueprints.posts.db.session.commit"
    ) as mock_commit:
        mock_add.return_value = None
        mock_commit.return_value = None

        test_client = create_test_app().test_client()
        response = test_client.post("/posts")
        assert response.status_code == codes.ok


#
# def test_put_post(client):
#     # creating a post
#     body = {"body": "Hello, world!"}
#     create_response_body = create_post(client, body)
#
#     # updating the post
#     url = "/post/{0}".format(create_response_body["id"])
#     body = {"body": "Jello, world!"}
#     put_response_body = request_json(client, "put", url, body)
#     assert body["body"] == put_response_body["body"]
