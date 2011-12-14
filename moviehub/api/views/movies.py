# -*- coding: utf-8 -*-
from flask import request, Response, make_response
import json

from moviehub.api import api # import our blueprint
from moviehub.core.models import Movie
from moviehub.api.utils import get_error_response, json_result



@api.route("/api/movies/<int:movie_id>/", methods=["GET"])
def show_movie(movie_id):
    """
    return a single movie by id

    get data
    ========
    :param      movie_id        id of the movie that should be returned

    """
    from moviehub.api import tmdb

    movie = Movie.get_by_id(movie_id)
    if not movie:
        return get_error_response(
            message="Could not find resource",
            status_code=404
        )
    #movies.get(movie_id)
    tmdb_data = tmdb.extract_movie_data(movie.imdb_id)

    movie_result = movie.to_dict()
    movie_result.update(
        image_url=tmdb_data.get("image_url", ""),
        description=tmdb_data.get("description", "")
    )

    return json_result(json.dumps(movie_result))

@api.route("/api/movies/")
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

@api.route("/api/movies/<int:id>/like", methods=["POST"])
def like_movie(id):
    movie = Movie.get_by_id(id)
    #if not movie:
    #    return get_error_response(
    #
    #    )
    return ""