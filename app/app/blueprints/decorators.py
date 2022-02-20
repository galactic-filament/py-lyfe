from functools import wraps


def role_required(role_name):
    print(role_name)

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            return fn(*args, **kwargs)

        return decorator

    return wrapper
