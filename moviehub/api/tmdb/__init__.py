# -*- coding: utf-8 -*-
import httplib2
import json
from moviehub.api import api

# http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/a314e35b02e9cad181b1f37c96989b95/tt0137523
url = "http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/a314e35b02e9cad181b1f37c96989b95/tt1340800"

http = httplib2.Http()
response, content = http.request(url)

in_dict = json.loads(content)[0]

def extract_movie_data(imdb_id):
    """
    Extracts description and image url for chosen movie

    When their api return empty result or an error occur
    we simply return a dict with blank values in image_url and description.
    """

    # TODO: add caching!

    url = "http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/%s/%s" % (api.tmdb_api_key, imdb_id)

    http = httplib2.Http()
    response, content = http.request(url)

    movie_data = json.loads(content)

    # we can't check the status code because they're sending 200 even
    # if no movie exists
    if movie_data[0] == "Nothing found.":
        return dict(
            image_url="",
            description="",
        )

    movie = dict()

    try:
        movie.update(description=movie_data[0].get("overview", "")) # set empty description if overview missing

        #movie.update(image_url=movie_data[0].get("posters"))
        for img in movie_data[0].get("posters"):
            image = img.get("image")
            if image.get("size") == "cover":
                movie.update(image_url=image.get("url"))
                return movie
    except:
        # return same result as when the movie doesn't exist in their db
        return dict(image_url="", description="")
    return dict(image_url="", description="")