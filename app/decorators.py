import os
from flask_login import current_user
from flask import abort
from functools import wraps


def admin_required(foo):
    @wraps(foo)
    def decorated(*args, **kwargs):
        if current_user.is_anonymous or current_user.email != os.environ.get('FLASK_MOVIE_ADMIN'):
            abort(403)
        return foo(*args, **kwargs)

    return decorated
