# -*- coding: utf-8 -*-
from functools import wraps
import httplib2
import urllib
import json

from moviehubapi import exceptions, security, models

class Moviehub(object):
    #API_URL = "http://localhost:8081/api"
    API_URL = "https://3.movie-hub.appspot.com/api"

    """
    This represent the HTTP API from Moviehub
    which aims to give easy access to all clients and client with user access APIs
    ...
    """

    def __init__(self, client_id, client_secret, access_token=None, redirect_uri=None):
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
    def required_access_token(f):
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

    @required_access_token
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

    def movie(self, id):
        """
        Give information about a single movie by given identifier.
        """
        response, movie_data = self._request("/movies/%d/" % id)
        return models.Movie.from_dict(json.loads(movie_data))
        #http = httplib2.Http()
        #response, content = http.request("http://localhost:8081/api/movies/%d/" % id)
        #response, content = http.request("https://3.movie-hub.appspot.com/api/movies/%d/" % id)
        #return models.Movie.from_dict(json.loads(content))


    def recent_movies(self, limit=10):
        http = httplib2.Http()
        #response, content = http.request("http://localhost:8080/api/movies/1/")
        response, content = http.request("https://3.movie-hub.appspot.com/api/latest_movies/")
        return content

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
            #body=urllib.urlencode([k, v.encode("utf-8")] for k,v in body.items())
            body=urllib.urlencode(body)
        response, content = http.request(self.API_URL + endpoint, method=method, headers=headers, body=body)

        return response, content



