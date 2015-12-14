import pytest
from app import server
from flask.ext.api import status
from flask import json


@pytest.fixture
def client():
    server.app.debug = True
    return server.app.test_client()


def _test_json(client, url, body):
    response = client.post(url, data=json.dumps(body),
                           content_type='application/json')
    assert status.is_success(response.status_code)
    response_body = json.loads(response.get_data(as_text=True))
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
    response_body = _test_json(client, '/reflection', body)
    assert response_body['greeting'] == body['greeting']
