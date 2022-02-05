from app.models import db


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(32))

    def as_dict(self):
        return {"id": self.id, "body": self.body}


def find_post_by_id(post_id):
    return Post.query.filter_by(id=post_id).first()
