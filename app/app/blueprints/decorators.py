from functools import wraps

from flask_jwt_extended import current_user
from werkzeug.exceptions import Unauthorized


def role_required(role_name):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            result = fn(*args, **kwargs)

            if current_user is None:
                raise Unauthorized()

            if role_name not in [x.name for x in current_user.user_roles]:

                raise Unauthorized()

            return result

        return decorator

    return wrapper
