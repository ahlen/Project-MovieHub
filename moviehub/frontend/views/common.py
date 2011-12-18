# -*- coding: utf-8 -*-
from flask import render_template, request, session, redirect

from moviehub.frontend import frontend, moviehub

#@frontend.route("/")
#def index():
#    return render_template("common/index.html")
from moviehub.frontend.utils import login_required

@frontend.route("/auth/")
def auth_code():
    if request.args.get("code"):
        token = moviehub.auth_exchange_token(request.args.get("code"))
        session["user_token"] = token
    return redirect("/")

@frontend.route("/login/")
def login():
    return redirect(moviehub.auth_code_url())

@frontend.route("/logout/")
@login_required
def logout():
    if "user_token" in session:
        session.pop("user_token", None)
    return redirect("/")

@frontend.route("/dev/api/")
def documentation():
    return render_template("/documentation/api.html")