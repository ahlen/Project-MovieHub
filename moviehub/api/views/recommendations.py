# -*- coding: utf-8 -*-
from flask import request, g

from google.appengine.ext import db

import json

from moviehub.api import api
from moviehub.core.models import Movie, Recommendation, RecommendationReview
from moviehub.api.utils import get_error_response

"""
GET /api/movies/{id}/recommendations/
POST /api/movies/{id}/recommendations/
GET /api/recommendations/{id}/
"""

@api.route("/api/movies/<int:movie_id>/recommendations/", methods=["POST"])
def add_recommendation(movie_id):
    target_movie_id = request.args.get("target_id", None)
    if not target_movie_id:
        return get_error_response(
            message="Missing required parameter: target_id",
            status_code=400 # bad request
        )
    if movie_id == int(target_movie_id):
        return get_error_response(
            message="Target and source cannot have the same id",
            status_code=400
        )

    # check if movies exists
    source = Movie.get_by_id(movie_id)
    target = Movie.get_by_id(int(target_movie_id))

    if not source or not target:
        return get_error_response(
            message="Could not find one of the resources",
            status_code=404
        )

    # check if recommendation already exists
    movies = [source.key(), target.key()]
    movies.sort()
    rec = Recommendation.all().filter("left = ", movies[0]).filter("right = ", movies[1]).get()

    if not rec:
        rec = Recommendation(
            rating=50,
            author=g.api_user,
            body="Hello World",
            movies=[source.key(), target.key()],
            left=movies[0],
            right=movies[1]
        )
        rec.put()

        return json.dumps(rec.to_dict())

    # otherwise the recommendation already exists
    return get_error_response(
        message="Recommendation already exists with %s (%d) and %s (%d)" % (source.title, source.key().id(), target.title, target.key().id()),
        status_code=400,
    )

@api.route("/api/movies/<int:movie_id>/recommendations/")
def get_recommendations(movie_id):
    movie = Movie.get_by_id(movie_id)
    if not movie:
        return get_error_response(
            message="Could not find the resource",
            status_code=404
        )

    recs = Recommendation.all().filter("movies = ", movie)

    return json.dumps([rec.to_dict() for rec in recs])

#@api.route("/api/recommendations/<int:id>/")
#def get_recommendation(id):
#    p = RecommendationPair.get_by_id(id)
#    return json.dumps(Recommendation.all().ancestor(p).get().to_dict())