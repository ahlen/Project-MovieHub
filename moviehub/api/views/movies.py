# -*- coding: utf-8 -*-
from flask import request, Response, make_response
import json
from flask.globals import g

from moviehub.api import api # import our blueprint
from moviehub.core.models import Movie
from moviehub.api.utils import get_error_response, json_result



@api.route("/api/movies/<int:id>/", methods=["GET"])
@api.require_client
def show_movie(id):
    """
    return a single movie by id

    path data
    =========
    :param      id        id of the movie that should be returned

    """
    from moviehub.api import tmdb

    movie = Movie.get_by_id(id)
    if not movie:
        return get_error_response(
            message="Could not find resource",
            status_code=404
        )

    tmdb_data = tmdb.extract_movie_data(movie.imdb_id)

    movie_result = movie.to_dict()
    movie_result.update(
        image_url=tmdb_data.get("image_url", ""),
        description=tmdb_data.get("description", "")
    )

    return json_result(json.dumps(movie_result))

@api.route("/api/movies/")
@api.require_client
def get_all_movies():
    """
    returns a list of all movies

    get data
    ========
    :param      include_remote      (optional) When set to true, the lists
                                    contains image_url and description
                                    if available from TMDb

    :param      limit               (optional) limit can be a positive integer
                                    without limit set, all data is loaded

    :param      only_ids            (optional) when only_ids is set the list of movies
                                    contains ids
    """

    limit = request.args.get("limit", None)
    include_remote = request.args.get("include_remote", False)
    only_ids = request.args.get("only_ids", False)

    if include_remote and include_remote == "true":
        include_remote = True
    else:
        include_remote = False

    if only_ids and only_ids == "true":
        only_ids = True
    else:
        only_ids = False

    if limit:
        try:
            limit = int(limit)

            if limit < 1:
                raise ValueError
        except (TypeError, ValueError):
            return get_error_response(
                message="optional parameter limit requires a positive integer",
                status_code=400
            )


    movies = Movie.all().order("title")
    if limit:
        movies = movies.fetch(limit=limit)

    return json_result(
        json.dumps([movie.to_dict(movie, include_remote=include_remote, only_id=only_ids) for movie in movies])
    )

@api.route("/api/movies/<int:id>/like/")
@api.require_user
def check_like_movie(id):
    """
    used to see if current user like selected movie

    path data
    =========
    :param      id      id of the movie that should be liked
    """
    like = Movie.gql("WHERE id = :1 AND likes = :2", id, g.api_user).get()
    if like:
        return "true"
    return "false"

@api.route("/api/movies/<int:id>/like/", methods=["POST", "DELETE"])
@api.require_user
def like_movie(id):
    """
    used to add or remove a like to a movie

    path data
    =========
    :param      id      id of the movie that should be liked
    """

    movie = Movie.get_by_id(id)
    if not movie:
        return get_error_response(
            message="Resource not found",
            status_code=404
        )
    try:
        if request.method == "POST":
            if not g.api_user.key() in movie.likes:
                movie.likes.append(g.api_user.key())
                movie.put()
        else:
            movie.likes.remove(g.api_user.key())
            movie.put()
    except ValueError:
        return get_error_response(
            message="User does not like this movie",
            status_code=400
        )
    return "true"