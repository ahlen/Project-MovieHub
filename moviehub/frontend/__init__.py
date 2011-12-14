# -*- coding: utf-8 -*-
from flask import Blueprint, session, g

from moviehubapi import Moviehub, models, exceptions

frontend = Blueprint("frontend", __name__, template_folder="templates")

# wrapper around moviehub REST api.
moviehub = Moviehub(client_id="10", client_secret="6230c1b6200f663733b256b35b23a5adf0d45b8b", access_token="abc")

import views

@frontend.before_request
def set_user():
    g.user = None
    if "user_id" in session:
        g.user = moviehub.me()