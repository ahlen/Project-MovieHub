# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify
from flask.helpers import url_for

import json

from moviehub.frontend import frontend, moviehub
from moviehub.frontend.utils import json_result
from werkzeug.utils import redirect

from wtforms import Form, TextField, validators

from moviehubapi import Moviehub, models, exceptions

@frontend.route("/movies/<int:id>/")
def show_movie(id):
    try:
        movie = moviehub.movie(id)
        recommendations = moviehub.recommendations(id)
    except exceptions.MoviehubApiError as ex:
        return "%s: %s" % (ex.type, ex.message)

    return render_template("movies/show.html", movie=movie, recommendations=recommendations)

@frontend.route("/_/movies/all/")
def get_modal_movies():
    movies = moviehub.movies()
    return json_result(
        json.dumps([{"title": movie.title, "id": movie.id} for movie in movies])
    )