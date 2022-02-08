import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(32))

    def as_dict(self):
        return {"id": self.id, "body": self.body}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(60))

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "hashed_password": self.password,
        }

    @classmethod
    def find_user(cls, username, password):
        found_user = User.query.filter_by(username=username).first()
        if found_user is None:
            return None

        password_matches = bcrypt.checkpw(password, found_user.password)
        if not password_matches:
            return None

        return found_user
