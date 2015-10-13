import server


def test_hello_world():
    client = server.app.test_client()
    rv = client.get('/')
    assert b'Hello World!' == rv.data
