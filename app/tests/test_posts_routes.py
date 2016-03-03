import pytest
from app import app
from tests import request_json, create_post


@pytest.fixture
def client():
    app.debug = True
    return app.test_client()


def test_posts(client):
    body = {'body': 'Hello, world!'}
    create_post(client, body)


def test_get_post(client):
    # creating a post
    body = {'body': 'Hello, world!'}
    create_response_body = create_post(client, body)

    # getting the post and asserting they match
    url = '/post/{0}'.format(create_response_body['id'])
    get_response_body = request_json(client, 'get', url)
    assert get_response_body['body'] == create_response_body['body']


def test_delete_post(client):
    # creating a post
    body = {'body': 'Hello, world!'}
    create_response_body = create_post(client, body)

    # deleting the post
    url = '/post/{0}'.format(create_response_body['id'])
    request_json(client, 'delete', url)


def test_put_post(client):
    # creating a post
    body = {'body': 'Hello, world!'}
    create_response_body = create_post(client, body)

    # updating the post
    url = '/post/{0}'.format(create_response_body['id'])
    body = {'body': 'Jello, world!'}
    put_response_body = request_json(client, 'put', url, body)
    assert body['body'] == put_response_body['body']
