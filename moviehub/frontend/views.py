# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.helpers import url_for

from moviehub.frontend import frontend
from werkzeug.utils import redirect

from wtforms import Form, TextField, validators

from moviehubapi import Moviehub, models

# wrapper around moviehub REST api.
moviehub = Moviehub(client_id="demo", client_secret="demo")

@frontend.route("/")
def index():

    from moviehub.core.models import Movie
    movies = []#Movie.get_movies()

    return render_template("base.html", movies=movies)

@frontend.route("/movies/<int:id>/")
def show_movie(id):
    movie = moviehub.movie(id)

    return render_template("movies/show.html", movie=movie)

class ArticleForm(Form):
    title = TextField("Title", validators=[validators.length(min=4, max=32)])
    content = TextField("Content", validators=[validators.length(min=4, max=4000)])

@frontend.route("/articles/new/", methods=["GET", "POST"])
def add_article():
    form = ArticleForm(request.form)

    if request.method == "POST" and form.validate():
        article = moviehub.add_article(
            title=form.title.data,
            content=form.content.data
        )
        return redirect(url_for("frontend.show_article", id=article.id))
    articles=moviehub.articles()
    
    return render_template("articles/new.html", form=form, articles=articles)

@frontend.route("/articles/<int:id>/")
def show_article(id):
    article = moviehub.article(id)

    return render_template("articles/show.html", article=article)
