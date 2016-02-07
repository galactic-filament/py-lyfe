import pytest
from app import server
from flask.ext.api import status
from flask import json


@pytest.fixture
def client():
    server.app.debug = True
    return server.app.test_client()


def _test_json(client, method, url, body=None):
    request = getattr(client, method)
    response = request(url, data=json.dumps(body),
                       content_type='application/json')
    assert status.is_success(response.status_code)
    response_body = json.loads(response.get_data(as_text=True))
    return response_body


def _create_post(client, body):
    response_body = _test_json(client, 'post', '/posts', body)
    assert type(response_body['id']) is int

    return response_body


def test_home(client):
    response = client.get('/')
    assert status.is_success(response.status_code)
    assert response.get_data(as_text=True) == 'Hello, world!'


def test_ping(client):
    response = client.get('/ping')
    assert status.is_success(response.status_code)
    assert response.get_data(as_text=True) == 'Pong'


def test_reflection(client):
    body = {'greeting': 'Hello, world!'}
    response_body = _test_json(client, 'post', '/reflection', body)
    assert response_body['greeting'] == body['greeting']


def test_posts(client):
    body = {'body': 'Hello, world!'}
    _create_post(client, body)


def test_get_post(client):
    # creating a post
    body = {'body': 'Hello, world!'}
    create_response_body = _create_post(client, body)

    # getting the post and asserting they match
    url = '/post/{0}'.format(create_response_body['id'])
    get_response_body = _test_json(client, 'get', url)
    assert get_response_body['body'] == create_response_body['body']


def test_delete_post(client):
    # creating a post
    body = {'body': 'Hello, world!'}
    create_response_body = _create_post(client, body)

    # deleting the post
    url = '/post/{0}'.format(create_response_body['id'])
    delete_response = _test_json(client, 'delete', url)
