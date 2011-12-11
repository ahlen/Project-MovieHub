# -*- coding: utf-8 -*-
from flask import request, Response, make_response, g
import json

from moviehub.api import api

@api.route("/api/me/")
def me():
    return json.dumps(g.api_user.to_dict())