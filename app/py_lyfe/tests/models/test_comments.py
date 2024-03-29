from uuid import uuid4

from py_lyfe.models import Comment, User, Post

mock_username = str(uuid4())
mock_password = "password"


def test_create_comment_happy_path(mock_db):
    comment = Comment()
    comment.body = "Hello, world!"
    mock_db.session.add(comment)

    user = User()
    user.username = mock_username
    user.set_password(mock_password)
    user.comments.append(comment)
    mock_db.session.add(user)

    post = Post()
    post.body = "Hello, world!"
    post.comments.append(comment)
    mock_db.session.add(post)

    mock_db.session.commit()

    user = User.find_user_by_username(mock_username)
    assert user is not None
    assert len(user.comments) == 1

    mock_db.session.delete(post)
    mock_db.session.commit()
