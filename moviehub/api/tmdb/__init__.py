# -*- coding: utf-8 -*-
import httplib2
import json
from google.appengine.api import memcache
from moviehub.api import api



def extract_movie_data(imdb_id):
    """
    Extracts description and image url for chosen movie

    When their api return empty result or an error occur
    we simply return a dict with blank values in image_url and description.
    """

    cache_key = "tmdb:%s" % imdb_id

    movie_cache = memcache.get(cache_key)
    if movie_cache:
        return movie_cache

    url = "http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/%s/%s" % (api.tmdb_api_key, imdb_id)

    http = httplib2.Http()
    response, content = http.request(url)

    movie_data = json.loads(content)

    # we can't check the status code because they're sending 200 even
    # if no movie exists
    if movie_data[0] == "Nothing found.":
        movie = dict(
            image_url="",
            description="",
        )
        memcache.set(cache_key, movie)
        return movie

    movie = dict()

    try:
        movie.update(description=movie_data[0].get("overview", "")) # set empty description if overview missing

        #movie.update(image_url=movie_data[0].get("posters"))
        for img in movie_data[0].get("posters"):
            image = img.get("image")
            if image.get("size") == "cover":
                movie.update(image_url=image.get("url"))
                memcache.set(cache_key, movie)
                return movie
    except:
        # return same result as when the movie doesn't exist in their db
        return dict(image_url="", description="")
    return dict(image_url="", description="")