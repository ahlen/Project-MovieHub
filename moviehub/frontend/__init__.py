# -*- coding: utf-8 -*-
from flask import Blueprint, session, g, request
from flask.helpers import flash

from moviehubapi import Moviehub

frontend = Blueprint("frontend", __name__, template_folder="templates")

# wrapper around moviehub RESTful api.

# used in deployed version
moviehub = Moviehub(client_id="19022", client_secret="d4e0ab3f53bc1ccd4aa86e722d73f672a3ef2635")

#moviehub = Moviehub(client_id="2", client_secret="d68346af469ab9deec068dc9c2f207b00542799a")

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
        session.pop("user_token", None)

    g.user = None
    moviehub.access_token = None
    if "user_token" in session:
        moviehub.access_token = session["user_token"]
        try:
            g.user = moviehub.me()
        except :
            session.pop("user_token", None)
            flash("Login expired, please login again", "warning")

@frontend.route("/set_token/")
def set_token():
    session["user_token"] = request.args.get("token", None)
    return "user_token=%s" % session["user_token"]