# -*- coding: utf-8 -*-
from flask import request, Response, make_response
import json

from moviehub.api import api # import our blueprint
from moviehub.core.models import Movie
from moviehub.api.utils import get_error_response

#movies = {
#    1: Movie(1, "Tinker Tailor Soldier Spy", "tt1340800"),
#    2: Movie(2, "New Year's Eve", "tt1598822"),
#    3: Movie(3, "Young Adult", "tt1625346"),
#    4: Movie(4, "The Sitter", "tt1366344"),
#    5: Movie(5, "W.E.", "tt1536048"),
#    6: Movie(6, "I Melt with You", "tt1691920"),
#    7: Movie(7, "We Need to Talk About Kevin", "tt1242460"),
#    8: Movie(8, "The Matrix", "tt0133093"),
#}

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

    return json.dumps(movie_result)

    #return json.dumps(tmdb.extract_movie_data("tt0137523"))
    # http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/a314e35b02e9cad181b1f37c96989b95/tt0137523
    #url = "http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/a314e35b02e9cad181b1f37c96989b95/tt0137523"

    #http = httplib2.Http()
    #response, content = http.request(url)

    #movie_data = json.loads(content)
    #if movie_data[0] == "Nothing found.":
    #    return "Could not find movie"

    #return str(movie_data)

    #poster = None
    #for img in in_dict.get("posters"):
    #    if img.get("")

    #return json.dumps(in_dict.get("posters")[0].get("image").get("url"))
    #return in_dict.get("posters")


    #return json.dumps(movies.get(movie_id).to_dict())

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