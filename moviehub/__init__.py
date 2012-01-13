# -*- coding: utf-8 -*-

from flask import Flask, redirect, request, session
from flask.helpers import url_for
import httplib2
from apiclient.discovery import build
from flask.globals import g

from moviehub.core.models import User, Client, AuthToken
import json

from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from oauth2client.client import AccessTokenCredentialsError

from google.appengine.api import urlfetch

try:
    from moviehub import local_settings as settings
except:
    from moviehub import settings

app = Flask(__name__)
app.config.from_object(settings)
app.secret_key = "somethingjustfordevelopment"

# register blueprints
from moviehub.api import api
from moviehub.frontend import frontend
app.register_blueprint(api)
app.register_blueprint(frontend)