# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.helpers import url_for

from moviehub.frontend import frontend, moviehub
from werkzeug.utils import redirect

from wtforms import Form, TextField, validators

from moviehubapi import Moviehub, models, exceptions

@frontend.route("/movies/<int:id>/recommendations/", methods=["POST"])
def add_recommendation_with_reason_from_movie(id):
    """
    Add recommendation if it doesn't already exists between the movies
    and in all scenarios it create a new reason for that recommendation
    """
    movies = "%d,%d" % (id, int(request.form.get("target_id")))

    reason = moviehub.add_reason(
        movie_ids=movies,
        body=request.form.get("motivation"),
        rating=request.form.get("rating"),
    )
    return redirect(url_for("frontend.recommendation", id=reason.recommendation.id))

@frontend.route("/recommendations/<int:id>/reasons/")
def add_reason(id):
    """
    Add new reason from recommendation
    """
    pass

@frontend.route("/recommendations/<int:id>/")
def show_recommendation(id):
    return render_template("recommendations/show.html")
