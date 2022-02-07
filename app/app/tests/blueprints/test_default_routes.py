import json

from requests import codes


def test_home(mock_client):
    response = mock_client.get("/")
    assert response.status_code == codes.ok
    assert response.get_data(as_text=True) == "Hello, world!"


def test_ping(mock_client):
    response = mock_client.get("/ping")
    assert response.status_code == codes.ok
    assert response.get_data(as_text=True) == "Pong"


def test_reflection(mock_client):
    body = {"greeting": "Hello, world!"}
    response = mock_client.post(
        "/reflection", data=json.dumps(body), content_type="application/json"
    )
    assert response.status_code == codes.ok

    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["greeting"] == body["greeting"]
