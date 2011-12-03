# -*- coding: utf-8 -*-
from flask import request, Response, make_response
import json

from moviehub.api import api

@api.route("/api/me/")
def me():
    pass
    # this should return the user that belongs to the auth_token