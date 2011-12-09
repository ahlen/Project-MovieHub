# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.helpers import url_for

from moviehub.frontend import frontend
from werkzeug.utils import redirect

from wtforms import Form, TextField, validators

from moviehubapi import Moviehub, models, exceptions

@frontend.route("/")
def index():

    from moviehub.core.models import Movie
    movies = []#Movie.get_movies()

    return render_template("base.html", movies=movies)