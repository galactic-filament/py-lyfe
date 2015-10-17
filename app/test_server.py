import pytest
import server
import json


@pytest.fixture
def client():
    server.app.debug = True
    return server.app.test_client()


def test_hello_world(client):
    response = client.get('/')
    assert b'Hello World!' == response.data


def test_404(client):
    response = client.get('/non-exist')
    assert response.status_code == 404


def test_receive_json(client):
    payload = {
        'title': 'Hello world!'
    }
    response = client.post(
        '/receive-json',
        data=json.dumps(payload),
        content_type='application/json'
    )

    d = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert d['title'] == payload['title']
