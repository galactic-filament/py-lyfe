import pytest
from app import app
from flask.ext.api import status
from tests import request_json


@pytest.fixture
def client():
    app.debug = True
    return app.test_client()


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
    response_body = request_json(client, 'post', '/reflection', body)
    assert response_body['greeting'] == body['greeting']
