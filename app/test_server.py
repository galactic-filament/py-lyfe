import pytest
import server


@pytest.fixture
def client():
    return server.app.test_client()


def test_hello_world(client):
    response = client.get('/')
    assert b'Hello World!' == response.data


def test_404(client):
    response = client.get('/non-exist')
    assert response.status_code == 404


def test_five_oh_oh(client):
    response = client.get('/five-oh-oh')
    assert response.status_code == 500


def test_login(client):
    response = client.get('/login')
    assert response.status_code == 500
