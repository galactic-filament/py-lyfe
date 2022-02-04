import json
from unittest.mock import patch

from requests import codes

from models.post import Post

mock_create_post_body = {"body": "Hello, world!"}
mock_post_id = 1


def test_get_post(mock_client):
    with patch("blueprints.posts.find_post_by_id") as mock_find_post_by_id:
        mock_post = Post()
        mock_post.id = mock_post_id
        mock_find_post_by_id.return_value = mock_post

        response = mock_client.get("/post/{0}".format(mock_post_id))
        assert response.status_code == codes.ok

        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"] == mock_post_id


def test_delete_post(mock_client):
    with patch("blueprints.posts.find_post_by_id") as mock_find_post_by_id, patch(
        "blueprints.posts.db.session.delete"
    ) as mock_delete, patch("blueprints.posts.db.session.commit") as mock_commit:
        mock_post = Post()
        mock_post.id = mock_post_id
        mock_find_post_by_id.return_value = mock_post

        mock_delete.return_value = None
        mock_commit.return_value = None

        response = mock_client.delete("/post/{0}".format(mock_post_id))
        assert response.status_code == codes.ok


def test_create_post(mock_client):
    with patch("blueprints.posts.db.session.add") as mock_add, patch(
        "blueprints.posts.db.session.commit"
    ) as mock_commit:

        def mock_add_side_effect(post):
            post.id = mock_post_id

        mock_add.side_effect = mock_add_side_effect
        mock_commit.return_value = None

        response = mock_client.post(
            "/posts",
            data=json.dumps(mock_create_post_body),
            content_type="application/json",
        )
        assert response.status_code == codes.created

        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"] == mock_post_id


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
