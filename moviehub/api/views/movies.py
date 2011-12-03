# -*- coding: utf-8 -*-
from flask import request, Response, make_response
import json

from moviehub.api import api # import our blueprint
from moviehub.core.models import Movie
from moviehub.api.utils import get_error_response

movies = {
    1: Movie(1, "Tinker Tailor Soldier Spy", "tt1340800"),
    2: Movie(2, "New Year's Eve", "tt1598822"),
    3: Movie(3, "Young Adult", "tt1625346"),
    4: Movie(4, "The Sitter", "tt1366344"),
    5: Movie(5, "W.E.", "tt1536048"),
    6: Movie(6, "I Melt with You", "tt1691920"),
    7: Movie(7, "We Need to Talk About Kevin", "tt1242460"),
}

@api.route("/api/movies/<int:movie_id>/", methods=["GET"])
def show_movie(movie_id):
    return json.dumps(movies.get(movie_id).to_dict())

@api.route("/api/latest_movies/")
def latest_movies():
    return json.dumps([m.to_dict() for m in movies.values()])
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