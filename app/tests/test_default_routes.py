import pytest
from requests import codes

from app import app
from tests import request_json


@pytest.fixture
def client():
    app.debug = True
    return app.test_client()


def test_home(client):
    response = client.get('/')
    assert response.status_code == codes.ok
    assert response.get_data(as_text=True) == 'Hello, world!'


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == codes.ok
    assert response.get_data(as_text=True) == 'Pong'


def test_reflection(client):
    body = {'greeting': 'Hello, world!'}
    response_body = request_json(client, 'post', '/reflection', body)
    assert response_body['greeting'] == body['greeting']
