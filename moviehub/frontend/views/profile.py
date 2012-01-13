# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect

from moviehub.frontend import frontend, moviehub
from moviehub.frontend.utils import login_required


@frontend.route("/me/")
@login_required
def profile():
    profile = moviehub.me()

    likes = moviehub.liked_movies()

    return render_template("profiles/likes.html", profile=profile, movies=likes)

@frontend.route("/users/<int:id>/")
def public_profile(id):
    try:
        profile = moviehub.profile(id)
    except :
        flash("User doesn't exists", "error")
        return redirect("/")

    likes = moviehub.liked_movies(id)

    return render_template("profiles/likes.html", profile=profile, movies=likes, profile_id=profile.id)

@frontend.route("/me/recommendations/")
@login_required
def profile_recommendations():
    profile = moviehub.me()

    recommendations = moviehub.user_recommendations()

    return render_template("/profiles/recommendations.html",
        profile=profile, recommendations=recommendations)

@frontend.route("/users/<int:id>/recommendations/")
def public_profile_recommendations(id):
    try:
        profile = moviehub.profile(id)
    except :
        flash("User doesn't exists", "error")
        return redirect("/")

    recommendations = moviehub.user_recommendations(id)

    return render_template("/profiles/recommendations.html",
        profile=profile, recommendations=recommendations, profile_id=profile.id)

@frontend.route("/me/reasons/")
@login_required
def profile_reasons():
    profile = moviehub.me()

    reasons = moviehub.user_reasons()

    return render_template("/profiles/reasons.html", profile=profile, reasons=reasons)

@frontend.route("/users/<int:id>/reasons/")
def public_profile_reasons(id):
    try:
        profile = moviehub.profile(id)
    except :
        flash("User doesn't exists", "error")
        return redirect("/")

    reasons = moviehub.user_reasons(id)

    return render_template("/profiles/reasons.html", profile=profile, reasons=reasons, profile_id=profile.id)


