# -*- coding: utf-8 -*-
from flask import Blueprint, session, g, request

from moviehubapi import Moviehub

frontend = Blueprint("frontend", __name__, template_folder="templates")

# wrapper around moviehub REST api.
moviehub = Moviehub(client_id="6", client_secret="a8825d04fa96c5610e5bbd06f7132ecddf32a9e8")

import views

@frontend.context_processor
def inject_user_and_api_client():
    return dict(
        user=g.user,
        moviehub=moviehub
    )

@frontend.before_request
def set_user():
    if request.args.get("delete")=="true":
        del session["user_token"]

    g.user = None
    moviehub.access_token = None
    if "user_token" in session:
        moviehub.access_token = session["user_token"]
        g.user = moviehub.me()

@frontend.route("/set_token/")
def set_token():
    session["user_token"] = request.args.get("token", None)
    return "user_token=%s" % session["user_token"]