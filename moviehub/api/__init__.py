# -*- coding: utf-8 -*-
from functools import wraps
import json
from flask import Blueprint, g, request
from moviehub.core.models import Client
from oauth2client.client import OAuth2WebServerFlow

try:
    from moviehub import local_settings as settings
except:
    from moviehub import settings

class ApiBlueprint(Blueprint):
    def require_client(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
        #    #if not g.remote_user or not g.remote_client:
        #    if not g.remote_client:
        #        return json.dumps({"error": "..."})
        #    return f(*args, **kwargs)

    def require_client_with_user(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
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
    # for now, simulate api check for client
    g.api_client = None
    if "client_id" in request.args and "client_token" in request.args and \
       request.args["client_id"] == "demo" and request.args["client_token"] == "demo":
        g.api_client = 1
        #g.api_client = Client()

    #if not "token" in request.args and request.args["token"] == "abc":
    #    g.remote_client = 1
    #    return
    #g.remote_client = None
    #if not "token" in request.args:
    #    g.remote_client = None
    #    return
    #else:
    #    if request.args["token"] == "abc":
    #        g.remote_client = 1