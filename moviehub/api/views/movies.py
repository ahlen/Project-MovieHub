# -*- coding: utf-8 -*-
from flask import request, Response, make_response
import json

from moviehub.api import api # import our blueprint
from moviehub.core.models import Movie
from moviehub.api.utils import get_error_response, json_result



@api.route("/api/movies/<int:movie_id>/", methods=["GET"])
def show_movie(movie_id):
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
    :param      include_remote      When set to true, the lists
                                    contains image_url and description
                                    if available from TMDb
    """



    movies = Movie.all().order("title")

    return json_result(
        json.dumps([movie.to_dict() for movie in movies])
    )


    #except:
    #return get_error_response("Hello world")

#    if movie_id % 2 == 0:
#        response = Response(
#            json.dumps({"error": {"type": "NoResourceFound", "message": "Could not find the resource"}}),
#            mimetype="application/json",
#            status=404
#        )
#
#        return response
#    else:
#        response = Response(
#            json.dumps(
#                {"movie":
#                    {"title": "Min film",
#                    "imdb_id": "tt137481231",
#                     }
#                }
#            ),
#            mimetype="application/json",
#            status=200
#        )
#
#        return response