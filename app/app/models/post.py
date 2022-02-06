from models import Post


def find_post_by_id(post_id):
    return Post.query.filter_by(id=post_id).first()
