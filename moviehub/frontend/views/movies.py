# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify, flash
from flask.helpers import url_for

import json

from moviehub.frontend import frontend, moviehub
from moviehub.frontend.forms import RecommendationForm
from moviehub.frontend.utils import json_result
from werkzeug.utils import redirect

from wtforms import Form, TextField, validators

from moviehubapi import Moviehub, models, exceptions

@frontend.route("/movies/<int:id>/", methods=["GET", "POST"])
def show_movie(id):
    form = RecommendationForm(request.form)
    try:
        if request.method == "POST" and form.validate():
            movies = "%d,%d" % (id, form.target_id.data)
            try:
                reason = moviehub.add_reason(
                    movie_ids=movies,
                    body=form.reason.data,
                    rating=form.rating.data,
                )
                return redirect(url_for("frontend.show_movie", id=id))
            except exceptions.MoviehubApiError as ex:
                flash(ex.message, "error")

        movie = moviehub.movie(id)
        recommendations = moviehub.recommendations(id)
    except exceptions.MoviehubApiError as ex:
        return "%s: %s" % (ex.type, ex.message)

    return render_template("movies/show.html", movie=movie, recommendations=recommendations, form=form)

@frontend.route("/_/movies/all/")
def get_modal_movies():
    movies = moviehub.movies()
    return json_result(
        json.dumps([{"title": movie.title, "id": movie.id} for movie in movies])
    )