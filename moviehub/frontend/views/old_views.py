# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.helpers import url_for

from moviehub.frontend import frontend, moviehub
from werkzeug.utils import redirect

from wtforms import Form, TextField, validators

from moviehubapi import Moviehub, models, exceptions

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

class ReviewForm(Form):
    title = TextField("Title", validators=[validators.length(min=1, max=32)])
    content = TextField("Content", validators=[validators.length(min=4, max=4000)])

@frontend.route("/reviews/new/", methods=["GET", "POST"])
def add_review():
    form = ReviewForm(request.form)

    if request.method == "POST" and form.validate():
        review = moviehub.add_review(
            title=form.title.data,
            content=form.content.data
        )
        return redirect(url_for("frontend.show_review", id=review.id))
    reviews=moviehub.reviews()

    return render_template("reviews/new.html", form=form, reviews=reviews)

@frontend.route("/reviews/<int:id>/")
def show_review(id):
    review = moviehub.review(id)

    return render_template("reviews/show.html", review=review)

