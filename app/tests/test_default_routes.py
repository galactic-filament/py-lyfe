import json

import pytest
from requests import codes

from tests import create_test_app


@pytest.fixture
def client():
    return create_test_app().test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == codes.ok
    assert response.get_data(as_text=True) == "Hello, world!"


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == codes.ok
    assert response.get_data(as_text=True) == "Pong"


def test_reflection(client):
    body = {"greeting": "Hello, world!"}
    response = client.post(
        "/reflection", data=json.dumps(body), content_type="application/json"
    )
    assert response.status_code == codes.ok

    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["greeting"] == body["greeting"]
