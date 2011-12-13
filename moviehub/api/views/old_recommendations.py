# -*- coding: utf-8 -*-
from flask import request, g

from google.appengine.ext import db

import json

from moviehub.api import api
from moviehub.core.models import Movie, Recommendation, RecommendationReview#, RecommendationPair
from moviehub.api.utils import get_error_response

"""
GET /api/movies/{id}/recommendations/
POST /api/movies/{id}/recommendations/
GET /api/recommendations/{id}/
"""

@api.route("/api/movies/<int:movie_id>/recommendations/", methods=["POST"])
def _old_add_recommendation(movie_id):
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
        def add_recommendation_with_review():
            """
            When new  recommendation is created and doesn't
            already exists
            """

            rec = Recommendation(
                rating=50,
                author=g.api_user,
                body="Hello World",
                movies=[source.key(), target.key()],
                left=movies[0],
                right=movies[1]
            )
            rec.put()

            review = RecommendationReview(
                recommendation=rec,
                author=rec.author,
                rating=rec.rating,
                score=0, #empty score because the post is new
                body=rec.body
            )
            review.put()

            return review

        review = db.run_in_transaction(add_recommendation_with_review())
        return json.dumps(review.to_dict(include_recommendation=True))
        #return json.dumps(rec.to_dict())

    # otherwise the recommendation already exists
    return get_error_response(
        message="Recommendation already exists with %s (%d) and %s (%d)" % (source.title, source.key().id(), target.title, target.key().id()),
        status_code=400,
    )

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

    # check if recommendation exists
    eq = Recommendation.check_uniqueness(source=source, target=target)

    if eq:
        def create_recommendations():

            p = RecommendationPair()
            p.put()

            r1 = Recommendation(parent=p, target=target, source=source, body="Hello World", rating=78, author=g.api_user)
            r1.put()
            r2 = Recommendation(parent=p, target=source, source=target, body="Hello World", rating=78, author=g.api_user)
            r2.put()

            return p.key().id()

        p_id = db.run_in_transaction(create_recommendations)

        return str(p_id)

        #return json.dumps(r.to_dict())

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

    recs = Recommendation.all().filter("source = ", movie).order("rating")

    return json.dumps([rec.to_dict() for rec in recs])

#@api.route("/api/recommendations/<int:id>/")
#def get_recommendation(id):
#    p = RecommendationPair.get_by_id(id)
#    return json.dumps(Recommendation.all().ancestor(p).get().to_dict())