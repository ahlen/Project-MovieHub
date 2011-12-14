# -*- coding: utf-8 -*-
from functools import wraps
import httplib2
import urllib
import json

from moviehubapi import exceptions, security, models

import os

class Moviehub(object):
    """
    This is a wrapper around the HTTP API from Moviehub
    which aims to give easy access to all clients and client with user access APIs
    """

    # TODO: just for dev. we need to use localhost...
    if os.environ['SERVER_SOFTWARE'].startswith('Development'):
        API_URL = "http://localhost:8081/api"
    else:
        API_URL = "https://movie-hub.appspot.com/api/"

    def __init__(self, client_id, client_secret, redirect_uri=None, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token

    # decorator to DRY the logic to check if
    # the endpoint require "client with user access"
    # so we can handle the such logic on client side
    # even if it's not necessary to handle here.
    def require_access_token(self):
        if not self.access_token:
            raise Exception("this method require an access_token")

    def info(self):
        """
        Give basic information about the client owner and
        basic information about the user if access_token is provided
        """
        response, content = self._client_request("/info/")
        if not response.status == 200:
            self._handle_error(content)

    # profiles
    # ========
    def me(self):
        self.require_access_token()

        pass

    # movies
    # ======

    def movies(self):
        """
        return a list of all movies within from moviehub
        """
        response, content = self._client_request("/movies/")
        if not response.status == 200:
            self._handle_error(content)
        return [models.Movie.from_dict(movie) for movie in json.loads(content)]

    def movie(self, id):
        """
        Give information about a single movie by given identifier.
        """
        response, content = self._client_request("/movies/%d/" % id)
        if not response.status == 200: # handle this when we not get ok response
            self._handle_error(content)

        return models.Movie.from_dict(json.loads(content))

    # recommendations/reasons
    # =======================

    def recommendations(self, movie_id):
        """
        get all recommendations for a movie
        """
        response, content = self._client_request("/movies/%d/recommendations/" % movie_id)
        if not response.status == 200:
            self._handle_error(content)
        return [models.Recommendation.from_dict(r) for r in json.loads(content)]

    def add_reason(self, movie_ids, rating, body):
        """
        add a new reason for a movie
        """
        self.require_access_token()

        reason = dict(movie_ids=movie_ids, rating=str(rating), body=body)
        response, content = self._user_request("/reasons/", method="POST", body=reason)

        if not response.status == 200:
            self._handle_error(content)

        return models.Reason.from_dict(json.loads(content))

    # internal helpers
    # ================

    def _client_request(self, endpoint, method="GET", body=None, headers=None):
        if headers is None:
            headers = dict()
        headers.update(
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        return self._request(endpoint, method, body, headers)

    def _user_request(self, endpoint, method="GET", body=None, headers=None):
        if headers is None:
            headers = dict()
        headers.update(
            token=self.access_token
        )

        return self._request(endpoint, method, body, headers)

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

    def _handle_error(self, data):
        error_data = json.loads(data).get("error")
        raise exceptions.MoviehubApiError(
            type=error_data.get("type"),
            message=error_data.get("message")
        )
