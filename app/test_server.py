import pytest
import server


@pytest.fixture
def client():
    return server.app.test_client()


def test_hello_world(client):
    rv = client.get('/')
    print(rv.data)
    assert b'Hello World!' == rv.data


def test_404(client):
    rv = client.get('/non-exist')
    assert rv.status_code == 404


def test_five_oh_oh(client):
    rv = client.get('/five-oh-oh')
    assert rv.status_code == 500
