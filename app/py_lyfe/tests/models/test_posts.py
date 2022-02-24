from uuid import uuid4

from py_lyfe.models import Post

mock_username = str(uuid4())
mock_password = "password"


def test_get_posts(mock_db):
    post = Post()
    post.body = "Hello, world"
    mock_db.session.add(post)

    mock_db.session.commit()

    posts = mock_db.session.query(Post).all()
    assert len(posts) == 1

    for post in posts:
        mock_db.session.delete(post)

    mock_db.session.commit()
