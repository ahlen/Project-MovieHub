# -*- coding: utf-8 -*-
from functools import wraps
import httplib2
import urllib
import json

from moviehubapi import exceptions, security, models

class Moviehub(object):
    API_URL = "http://localhost:8081/api"
    #API_URL = "https://movie-hub.appspot.com/api"

    """
    This represent the HTTP API from Moviehub
    which aims to give easy access to all clients and client with user access APIs
    ...
    """

    def __init__(self, client_id, client_secret, redirect_uri=None, access_token=None):
        if not client_id and not secret:
            raise Exception("You need to provide both client_id and secret " \
                            "which you can find on https://movie-hub.appspot.com/admin/apps/")
        self.client_id = client_id
        self.client_secret = client_secret

        # these may be used within kwargs...
        self.access_token = access_token
        self.redirect_uri = redirect_uri

    # decorator to DRY the logic to check if
    # the endpoint require "client with user access"
    # so we can handle the such logic on client side
    # even if it's not necessary to handle here.
    def require_access_token(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            pass # check logic
        return decorated_function

    def info(self):
        """
        Give basic information about the client owner and
        basic information about the user if access_token is provided
        """
        pass

    @require_access_token
    def me(self, access_token=None):
        """
        Give basic information about the user if access_token is provided
        """
        pass

    def articles(self):
        response, content = self._request("/articles/", method="GET")
        articles_dict = json.loads(content)
        articles=[]
        for article in articles_dict:
            articles.append(models.Article.from_dict(article))
        return articles
        #article_data = self._request("articles/")
        #return models.

    def add_article(self, title, content):
        article_data = {"title": title, "content": content}
        response, content = self._request("/articles/", method="POST", body=article_data)

        return models.Article.from_dict(json.loads(content))

    def article(self, id):
        response, content = self._request("/articles/%d/" % id, method="GET")
        #return content
        return models.Article.from_dict(json.loads(content))

    def reviews(self):
        response, content = self._request("/reviews/", method="GET")
        reviews_dict = json.loads(content)
        reviews=[]
        for review in reviews_dict:
            reviews.append(models.Review.from_dict(review))
        return reviews

    def add_review(self, title, content):
        review_data = {"title": title, "text": content}
        response, content = self._request("/reviews/", method="POST", body=review_data)

        return models.Review.from_dict(json.loads(content))

    def review(self, id):
        response, content = self._request("/reviews/%d/" % id, method="GET")
        #return content
        return models.Review.from_dict(json.loads(content))

    def movie(self, id):
        """
        Give information about a single movie by given identifier.
        """
        response, movie_data = self._request("/movies/%d/" % id)
        if not response.status == 200: # handle this when we not get ok response
            error_data = json.loads(movie_data).get("error")
            raise exceptions.MoviehubApiError(
                type=error_data.get("type"),
                message=error_data.get("message")
            )

        return models.Movie.from_dict(json.loads(movie_data))

    def movies(self, limit=100):
        """
        Get all movies from the API
        """
        response, movies_data = self._request("/movies/")
        if not response.status == 200:
            error_data = json.loads(movie_data).get("error")
            raise exceptions.MoviehubApiError(
                type=error_data.get("type"),
                message=error_data.get("message")
            )
        return [models.Movie.from_dict(movie) for movie in json.loads(movies_data)]

    def recommendations(self, movie_id):
        response, content = self._request("/movies/%d/recommendations/" % movie_id)
        rec_data = json.loads(content)
        if not response.status == 200:
            error_data = rec_data.get("error")
            raise exceptions.MoviehubApiError(
                type=error_data.get("type"),
                message=error_data.get("message")
            )
        return [models.Recommendation.from_dict(r) for r in rec_data]

    def add_recommendation_review(self, movie_ids, rating, body):
        recommendation_data = {"movie_ids": movie_ids, "rating": rating, "body": body}
        response, content = self._request("/reasons/", method="POST", body=recommendation_data)

        return content
        #return models.Recommendation.from_dict(json.loads(content))

    def _client_request(self, endpoint, method="GET", body=None, headers=None):
        """
        Helper method for calling API endpoints which require client access
        """
        # TODO: add client request headers
        return _request(self, endpoint, method, body, headers)

    def _request(self, endpoint, method="GET", body=None, headers=None):
        http = httplib2.Http()

        # check if the method have a slash
        # in the beginning and remove it if it have that.
        if endpoint and endpoint[0] != "/":
            endpoint = "/" + endpoint
        if body:
            # thanks to http://stackoverflow.com/a/788055
            body=urllib.urlencode(dict([k, v.encode('utf-8')] for k, v in body.items()))
            #body=urllib.urlencode(body)
        response, content = http.request(self.API_URL + endpoint, method=method, headers=headers, body=body)

        return response, content



