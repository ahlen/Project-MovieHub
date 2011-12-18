# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.helpers import url_for, flash

from moviehub.frontend import frontend, moviehub
from moviehub.frontend.forms import ReasonForm
from moviehub.frontend.utils import login_required
from werkzeug.utils import redirect

from wtforms import Form, TextField, validators

from moviehubapi import Moviehub, models, exceptions

@frontend.route("/movies/<int:id>/recommendations/", methods=["POST"])
@login_required
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

@frontend.route("/reasons/<int:id>/vote/", methods=["POST"])
@login_required
def add_reason_vote(id):
    """
    Add or update vote for reason
    """
    if request.form.get("vote_btn", "") == "up":
        vote_type="up"
    elif request.form.get("vote_btn", "") == "down":
        vote_type="down"

    check_vote = moviehub.check_reason_vote(id)
    if check_vote:
        if vote_type+"vote" == check_vote.vote:
            try:
                moviehub.remove_reason_vote(id)
            finally:
                return redirect(url_for("frontend.show_recommendation", id=check_vote.reason.recommendation.id))
        else:
            vote = moviehub.reason_vote(id, vote_type)
    else:
        vote = moviehub.reason_vote(id, vote_type)

    if not vote:
        flash("Could not vote on non existing reason", "error")
        redirect("/")
    return redirect(url_for("frontend.show_recommendation", id=vote.reason.recommendation.id))

@frontend.route("/recommendations/<int:id>/", methods=["GET", "POST"])
def show_recommendation(id):
    recommendation = moviehub.recommendation(id)
    if not recommendation:
        flash("Recommendation not found", "warning")
        redirect("/")

    form = ReasonForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            reason = moviehub.add_reason(
                movie_ids="%d,%d" % (recommendation.movies[0].id, recommendation.movies[1].id),
                rating=form.rating.data,
                body=form.reason.data
            )
        except exceptions.MoviehubApiError as ex:
            flash(ex.message)
            return redirect(url_for("frontend.show_recommendation", id=id))

    reasons = moviehub.reasons(recommendation.id)

    return render_template("recommendations/show.html",
        recommendation=recommendation,
        reasons=reasons,
        form=form
    )