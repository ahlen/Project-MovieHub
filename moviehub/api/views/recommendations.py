# -*- coding: utf-8 -*-
from flask import request, g

from google.appengine.ext import db

import json

from moviehub.api import api
from moviehub.core.models import Movie, Recommendation, RecommendationReason, ReasonVote
from moviehub.api.utils import get_error_response

@api.route("/api/reasons/", methods=["POST"])
@api.require_user
def add_recommendation_reason():
    """
    add new recommendation reason to two movies
    and if the relationship doesn't exists we create it too.

    post data
    =========
    :param  movie_ids       require a comma-separated list of two movie ids
                            example: movie_ids=1,2

    :param  body            require a string with length between 4 and 1024
    :param  rating          require a integer between 0 to 100

    """
    movies = request.form.get("movie_ids", None)
    if not movies:
        return get_error_response(
            message="Missing required parameter movie_ids",
            status_code=400
        )

    # we may improve the DRY later
    body, rating = request.form.get("body", None), request.form.get("rating", None)

    if not body:
        return get_error_response(
            message="Missing required parameter body",
            status_code=400
        )
    if not rating:
        return get_error_response(
            message="Missing required parameter rating",
            status_code=400
        )

    if not (4 <= len(body) <= 1024):
        return get_error_response(
            message="Body can only be between 4 and 1024 characters",
            status_code=400
        )

    try:
        rating = int(rating)

        if not 0 <= rating <= 100:
            raise ValueError() # just for DRY because exceptions are free...right.
    except:
        return get_error_response(
            message="Rating must be an integer between 0 and 100",
            status_code=400
        )

    try:
        # get only two items from the list because the user may put
        # more movies on it but we only support two, at least at the moment.
        # because we may want to support users to create recommendations for all
        # permutations in the feature...
        movies = [int(mid) for mid in movies.split(",")[0:2]]
        if not len(movies) == 2:
            return get_error_response(
                message="Input of movie_ids required two id numbers",
                status_code=400
            )

        if movies[0] == movies[1]:
            return get_error_response(
                message="movie_ids cannot be the same",
                status_code=400
            )

        movie_left, movie_right = Movie.get_by_id(movies)

        if not movie_left or not movie_right:
            return get_error_response(
                message="Could not find one of the resources",
                status_code=400
            )

        movie_keys = [movie_left.key(), movie_right.key()]
        movie_keys.sort()

        rec = Recommendation.all().filter("left = ", movie_keys[0])\
        .filter("right = ", movie_keys[1]).get()

        # if recommendation doesn't already exists
        if not rec:
            r = Recommendation(
                rating=rating,
                author=g.api_user,
                body=body,
                movies=movie_keys,
                left=movie_keys[0],
                right=movie_keys[1]
            )
            r.put()

            reason = RecommendationReason(
                recommendation=r,
                author=r.author,
                rating=rating,
                score=0.0, #empty score because the post is new
                body=body
            )
            reason.put()

            r.current_reason=reason
            r.put()

            return json.dumps(reason.to_dict())

        if RecommendationReason.gql("WHERE author = :1 AND recommendation = :2", g.api_user, rec).get():
            return get_error_response(
                message="Each author can only write one reason per recommendation",
                status_code=400
            )

        # otherwise we create a new reason with the recommendation as "parent"
        reason = RecommendationReason(
            recommendation=rec,
            rating=rating,
            author=g.api_user,
            score=0.0,
            body=body
        )
        reason.put()

        return json.dumps(reason.to_dict())

    except ValueError:
        return get_error_response(
            message="Input of movie_ids is not valid (can only be a list of two ids like 1,2)",
            status_code=400
        )


@api.route("/api/reasons/<int:id>/", methods=["PUT"])
@api.require_user
def edit_recommendation_reason(id):
    """
    edit an existing reason

    path data
    =========
    :param      id              id of the reason to update

    put data
    ========
    :param      body            require a string with length between 4 and 1024
    :param      rating          require a integer between 0 to 100

    """

    reason = RecommendationReason.get_by_id(id)
    if not reason:
        return get_error_response(
            message="Resource not found",
            status_code=404
        )
    if not reason.author == g.api_user:
        return get_error_response(
            message="No permission",
            status_code=403 # forbidden
        )

    return "TODO: implement logic to edit"


@api.route("/api/reasons/<int:reason_id>/vote/", methods=["POST"])
@api.require_user
def add_reason_vote(reason_id):
    """
    Add or update vote for a recommendation reason.

    post data
    =========
    :param  vote        require either "up" or "down"

    """
    vote = request.form.get("vote", None)
    if not vote or not vote in ("up", "down"):
        return get_error_response(
            message="Missing required parameter vote or its value is not any of \"up\" or \"down\"",
            status_code=400
        )

    vote_score = {"up": 1, "down": -1}[vote]

    reason = RecommendationReason.get_by_id(reason_id)
    if not reason:
        return get_error_response(
            message="Resource not found",
            status_code=404
        )

    rev_vote = ReasonVote.make_vote(vote_score, g.api_user, reason)
    if rev_vote:
        return json.dumps(rev_vote.to_dict())
    return get_error_response(
        message="Could not make vote",
        status_code=400
    )


@api.route("/api/reasons/<int:reason_id>/vote/", methods=["DELETE"])
@api.require_user
def delete_reason_vote(reason_id):
    reason = RecommendationReason.get_by_id(reason_id)
    if not reason:
        return get_error_response(
            message="Resource not found",
            status_code=404
        )

    vote = ReasonVote.delete_vote(g.api_user, reason)
    if vote:
        return json.dumps(vote.to_dict())

    return get_error_response(
        message="Resource not found",
        status_code=404
    )


@api.route("/api/reasons/<int:reason_id>/vote/")
@api.require_user
def get_vote_for_reason(reason_id):
    """
    get the current users vote data if it exists
    """
    reason = RecommendationReason.get_by_id(reason_id)
    if not reason:
        return get_error_response(
            message="Resource not found",
            status_code=404
        )
    vote = ReasonVote.gql("WHERE ANCESTOR is :1 AND author = :2", reason, g.api_user)
    if vote:
        return json.dumps(vote.to_dict())

    return get_error_response(
        message="Resource not found",
        status_code=404
    )


@api.route("/api/movies/<int:movie_id>/recommendations/")
@api.require_client
def get_recommendations(movie_id):
    movie = Movie.get_by_id(movie_id)
    if not movie:
        return get_error_response(
            message="Could not find the resource",
            status_code=404
        )

    recs = Recommendation.all().filter("movies = ", movie).order("-rating")

    return json.dumps([rec.to_dict() for rec in recs])


@api.route("/api/reasons/<int:id>/")
@api.require_client
def get_reason(id):
    return json.dumps(RecommendationReason.get_by_id(id).to_dict())


@api.route("/api/recommendations/exists/")
@api.require_client
def get_recommendation_exists():
    """
    Check if a recommendation between two movies exists

    get data
    ========
    :param      movie_ids       require a comma-separated list of two movie ids
                                example: movie_ids=1,2
    """

    movies = request.args.get("movie_ids", None)
    if not movies:
        return get_error_response(
            message="Missing required parameter movie_ids",
            status_code=400
        )

    try:
        movies = [int(mid) for mid in movies.split(",")[0:2]]
        if not len(movies) == 2:
            return get_error_response(
                message="Input of movie_ids required two id numbers",
                status_code=400
            )
    except ValueError:
        return get_error_response(
            message="Input of movie_ids required two id numbers",
            status_code=400
        )

    if movies[0] == movies[1]:
        return get_error_response(
            message="movie_ids cannot be the same",
            status_code=400
        )

    movie_left, movie_right = Movie.get_by_id(movies)

    if not movie_left or not movie_right:
        return get_error_response(
            message="Could not find one of the resources",
            status_code=400
        )

    movie_keys = [movie_left.key(), movie_right.key()]
    movie_keys.sort()

    rec = Recommendation.all().filter("left = ", movie_keys[0])\
    .filter("right = ", movie_keys[1]).get()

    if rec:
        return "True"
    return "False"