from flask import abort
from flask_login import current_user
from functools import wraps

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.get_id() != '1':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function