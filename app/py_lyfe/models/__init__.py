import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app, db_uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(32))

    comments = db.relationship(
        "Comment", back_populates="post", cascade="delete"
    )

    def as_dict(self):
        return {"id": self.id, "body": self.body}

    @classmethod
    def find_post_by_id(cls, post_id):
        return Post.query.filter_by(id=post_id).first()

    @classmethod
    def find_all(cls):
        return Post.query.all()


user_roles = db.Table(
    "user_roles",
    db.Column(
        "user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True
    ),
    db.Column(
        "role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True
    ),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    hashed_password = db.Column(db.String(60))

    comments = db.relationship("Comment", back_populates="user")
    user_roles = db.relationship(
        "Role",
        secondary=user_roles,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "hashed_password": self.hashed_password,
        }

    def set_password(self, next_password):
        self.hashed_password = bcrypt.hashpw(
            next_password.encode(), bcrypt.gensalt()
        ).decode()

    @classmethod
    def find_user_matching_password(cls, username, password):
        found_user = User.query.filter_by(username=username).first()
        if found_user is None:
            return None

        password_matches = bcrypt.checkpw(
            password.encode(), found_user.hashed_password.encode()
        )
        if not password_matches:
            return None

        return found_user

    @classmethod
    def find_user_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def clear_test_users(cls, username_prefix):
        like_clause = "{0}%".format(username_prefix)

        users = User.query.filter(User.username.like(like_clause)).all()
        total_deleted = 0
        for user in users:
            db.session.delete(user)
            db.session.commit()

            total_deleted += 1

        return total_deleted


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(32))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="comments")
    post = db.relationship("Post", back_populates="comments")

    def as_dict(self):
        return {"id": self.id, "body": self.body, "post_id": self.post_id}

    @classmethod
    def find_comment_by_id(cls, comment_id):
        return Comment.query.filter_by(id=comment_id).first()
