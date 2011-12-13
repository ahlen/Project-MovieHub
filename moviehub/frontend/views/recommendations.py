# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.helpers import url_for

from moviehub.frontend import frontend, moviehub
from werkzeug.utils import redirect

from wtforms import Form, TextField, validators

from moviehubapi import Moviehub, models, exceptions

@frontend.route("/movies/<int:id>/recommendations/", methods=["POST"])
def add_review(id):
    movies = "%d,%d" % (id, int(request.form.get("target_id")))

    return moviehub.add_recommendation_review(
        movie_ids=movies,
        body=request.form.get("motivation"),
        rating=request.form.get("rating"),
    )