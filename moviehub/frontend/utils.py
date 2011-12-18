# -*- coding: utf-8 -*-
from functools import wraps
from flask import Response, redirect
from flask.globals import g
from flask.helpers import flash

def json_result(data, status_code=200):
    """
    return a result with application/json as mime-type
    """
    return Response(
        data,
        mimetype="application/json",
        status=status_code
    )

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            flash("You need to be logged in to perform that action", "warning")

            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function