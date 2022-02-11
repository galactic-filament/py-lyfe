from uuid import uuid4

from models import User, Comment, Post

mock_username = str(uuid4())
mock_password = "password"


def test_create_comment_happy_path(mock_db):
    user = User()
    user.username = mock_username
    user.set_password(mock_password)
    mock_db.session.add(user)
    mock_db.session.commit()

    post = Post()
    post.body = "Hello, world!"
    mock_db.session.add(post)
    mock_db.session.commit()

    comment = Comment()
    comment.body = "Hello, world!"
    comment.user_id = user.id
    comment.post_id = post.id
    mock_db.session.add(comment)
    mock_db.session.commit()
