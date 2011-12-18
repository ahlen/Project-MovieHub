# -*- coding: utf-8 -*-
from flask import request, Response, make_response, g
import json

from moviehub.core.models import User
from moviehub.api import api
from moviehub.api.utils import get_error_response

@api.route("/api/me/")
@api.require_user
def me():
    return json.dumps(g.api_user.to_dict())

@api.route("/api/profiles/<int:id>/")
def profile(id):
    user = User.get_by_id(id)
    if not user:
        get_error_response(
            message="Resource not found",
            status_code=404
        )

    return json.dumps(user.to_dict())