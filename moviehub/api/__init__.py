# -*- coding: utf-8 -*-
from functools import wraps
import json
from flask import Blueprint, g, request
from moviehub.api.utils import get_error_response
from moviehub.core.models import Client, User
from oauth2client.client import OAuth2WebServerFlow

try:
    from moviehub import local_settings as settings
except:
    from moviehub import settings

class ApiBlueprint(Blueprint):
    def require_client(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.api_client:
                return get_error_response(
                    message="Not a valid client ",
                    status_code=400
                )
            return f(*args, **kwargs)
        return decorated_function

    def require_user(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.api_user:
                return get_error_response(
                    message="Not valid user token",
                    status_code=400
                )
            return f(*args, **kwargs)
        return decorated_function

    @property
    def tmdb_api_key(self):
        try:
            from moviehub.local_settings import TMDB_API_KEY
        except:
            from moviehub.settings import TMDB_API_KEY

        return TMDB_API_KEY

    @property
    def google_oauth(self):
        oauth = OAuth2WebServerFlow(
            client_id=settings.GOOGLE_OAUTH2_ID,#"",#app.config.GOOGLE_OAUTH2_ID,
            client_secret=settings.GOOGLE_OAUTH2_SECRET,#"",#app.config.GOOGLE_OAUTH2_SECRET,
            scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
            redirect_uri="https://movie-hub.appspot.com/oauth2callback",
        )
        return oauth

api = ApiBlueprint("api", __name__)

#from views import movies # so our routes are added to central routing.

import views

@api.before_request
def set_client_and_user_access():
    """
    Check and set if the api calls have required
    headers to perform each call
    """
    g.api_client = None
    g.api_user = None

    client_id = request.headers.get("client_id", None) or request.args.get("client_id", None)
    client_secret = request.headers.get("client_secret", None) or request.args.get("client_secret", None)

    if client_id and client_secret:
        client = True
        #client = Client.gql("WHERE id = :1 AND client_secret = :2", client_id, client_secret).get()
        if client:
            g.api_client = Client.all().get()

    token = request.headers.get("token", None) or request.args.get("token", None)
    if token and token == "abc":
        g.api_user = User.all().get()