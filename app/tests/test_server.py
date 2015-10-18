import pytest
import json
from app import server, arithmetic
import functools


@pytest.fixture
def client():
    server.app.debug = True
    return server.app.test_client()


def test_hello_world(client):
    response = client.get('/')
    assert 'Hello World!' == response.get_data(as_text=True)


def test_404(client):
    response = client.get('/non-exist')
    assert response.status_code == 404


def test_receive_json(client):
    payload = {'title': 'Hello world!'}
    response = client.post(
        '/receive-json',
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == 200
    d = json.loads(response.get_data(as_text=True))
    assert d['title'] == payload['title']


def test_add(client):
    numbers = range(1, 10)
    payload = {'numbers': list(numbers)}
    response = client.post(
        '/add',
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == 200
    d = json.loads(response.get_data(as_text=True))
    assert d['sum'] == functools.reduce(arithmetic.add, numbers)
