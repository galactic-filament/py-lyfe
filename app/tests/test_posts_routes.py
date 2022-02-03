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


# def test_posts(mock_client):
#     with patch.object(MockDao, "add") as mock_method:
#
#         def side_effect(post):
#             post.id = mock_post_id
#
#         mock_method.side_effect = side_effect
#
#         response = mock_client.post(
#             "/posts",
#             data=json.dumps(mock_create_post_body),
#             content_type="application/json",
#         )
#         assert response.status_code == codes.created
#
#         response_body = json.loads(response.get_data(as_text=True))
#         assert response_body["id"] == mock_post_id


# def test_delete_post(client):
#     # creating a post
#     body = {"body": "Hello, world!"}
#     create_response_body = create_post(client, body)
#
#     # deleting the post
#     url = "/post/{0}".format(create_response_body["id"])
#     request_json(client, "delete", url)
#
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
