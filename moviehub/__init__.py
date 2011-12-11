# -*- coding: utf-8 -*-

from flask import Flask, redirect, request, session
from flask.helpers import url_for
import httplib2
from apiclient.discovery import build
from flask.globals import g

from moviehub.core.models import User
import json

from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from oauth2client.client import AccessTokenCredentialsError

from google.appengine.api import urlfetch

try:
    from moviehub import local_settings as settings
except:
    from moviehub import settings

from moviehub import local_settings

app = Flask(__name__)
#app.config.from_object(settings)
app.secret_key = "something just for development"

# register blueprints
from moviehub.api import api
from moviehub.frontend import frontend
app.register_blueprint(api)
app.register_blueprint(frontend)

# TODO: move client_id and client_secret to local settings
# to hide from public repository

#@app.before_request
#def set_user():
#    g.user = None
#    if "user_id" in session:
#        g.user = User.get_by_id(session["user_id"])
"""
@app.route("/")
def index():
    if g.user:
        username = g.user.full_name
    else:
        username = "Anonymous <a href=\"%s\">(Login)</a>" % url_for("login")

    return "Hello %s" % username

@app.route("/ping/<int:number>")
def ping(number):
    return "You pinged: %d" % (number)
"""

#@app.route("/auth/login/")
#def login():
#    return "<a href=\"%s\">Login</a>" % (api.google_oauth.step1_get_authorize_url(redirect_uri="https://3.movie-hub.appspot.com/oauth2callback"))

# TODO: move this to core.
#@app.route("/oauth2callback")
def request_token():
    #try: # try to redeem an access token
    if "code" in request.args:
        try:
            cred = oauth.step2_exchange(request.args.get("code"))
        except FlowExchangeError:
            return "Raised FlowExchangeError :)"

        user_data = json.loads(urlfetch.fetch(
            url="https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": "Bearer " + cred.access_token}).content
        )

        try:
            user = User.gql("where email = :1", user_data["email"]).fetch(1).pop()

            user.access_token = cred.access_token
            user.token_expiry = cred.token_expiry
            user.refresh_token = cred.refresh_token
            # update picture just in case...
            user.photo_url=user_data["picture"]
            user.put()

            session["user_id"] = user.key().id()
        except IndexError:
            user = User(
                # we need to save access_token and related for upcoming
                # api calls
                access_token=cred.access_token,
                token_expiry=cred.token_expiry,
                refresh_token=cred.refresh_token,
                # we save email, name and id from the user_data dict
                full_name=user_data.get("name", user_data["id"]), # try to get name, otherwise we use the id
                google_id=user_data["id"],
                photo_url=user_data["picture"],
                email=user_data["email"]
            )
            user.put()

            # set the user id to our session to set the user logged in.
            session["user_id"] = user.key().id()

        # redirect back to the main page
        return redirect("/")

    else: # probably error return... may fix this later.
        return "Could not get access token :)"
    #except Exception as ex:
    #    return ex.message
        
    """data = []

    data.append(cred.to_json())

    user = User(
        access_token=cred.access_token,
        token_expiry=cred.token_expiry,
        refresh_token=cred.refresh_token
    )

    # get the email and name from the g+ api.
    http = httplib2.Http()
    http = cred.authorize(http)
    service = build("plus", "v1", http=http)

    person = service.people().get(userId="me").execute(http)

    user.google_id = person.get("id")
    user.full_name = person.get("displayName")

    data.append(person)

    user.put()
    """

    #session["user_id"] = user.key().id()

    #return json.dumps(data)

@app.route("/_data/add/")
def add_sample_data():
    from moviehub.core.models import Movie, Client
    from moviehub.core.models import Review
    from google.appengine.ext import db

    """
    movies = [
        Movie(title="Tinker Tailor Soldier Spy", imdb_id="tt1340800"),
        Movie(title="New Year's Eve", imdb_id="tt1598822"),
        Movie(title="Young Adult", imdb_id="tt1625346"),
        Movie(title="The Sitter", imdb_id="tt1366344"),
        Movie(title="W.E.", imdb_id="tt1536048"),
        Movie(title="I Melt with You", imdb_id="tt1691920"),
        Movie(title="We Need to Talk About Kevin", imdb_id="tt1242460"),
        Movie(title="The Matrix", imdb_id="tt0133093"),
    ]
    #db.put_async(movies)
    for m in movies:
        m.put()
    """

    #client = Client(redirect_uri="http://www.demo.se", name="Demo", secret="TEST", user=)
    #review = [
    #    Review(title="Oldboy", text="Korean film, very good!", rating=9),
    #    Review(title="Kiss Kiss Bang Bang", text="Action/Comedy with Downey Jr", rating=8),
    #]

    #for m in review:
    #    m.put()


    u = User(email="mikael.ahlen@gmail.com",
        full_name="Mikael Ahlen",
        photo_url="https://lh4.googleusercontent.com/-kPBDOS79uEk/AAAAAAAAAAI/AAAAAAAAAC4/N23-_zPoMMg/photo.jpg",
        google_id="111331274520904684671",
        access_token="ya29.AHES6ZStvSU0dsoexKVyMGVvTcWiB6O1cPhpU4gBqWk5t2F2o1Xr",
        refresh_token="1/E2w6hL8_GPKaMJ6A3Mem7dyK1Sfco2YrL3sKuBcInFk",
    )

    u.put()

    return "User: " + str(u.key().id())


    #client = Client(redirect_uri="http://localhost:8080/login/", name="Moviehub")
    #client.generate_secret()
    #client.put()

    #return "Added demo data"
    #for m in movies:
    #    m.put()
