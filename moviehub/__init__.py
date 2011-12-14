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
    #from moviehub.core.models import Review
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
    u = User(email="mikael.ahlen@gmail.com",
        full_name="Mikael Ahlen",
        photo_url="https://lh4.googleusercontent.com/-kPBDOS79uEk/AAAAAAAAAAI/AAAAAAAAAC4/N23-_zPoMMg/photo.jpg",
        google_id="111331274520904684671",
        access_token="ya29.AHES6ZStvSU0dsoexKVyMGVvTcWiB6O1cPhpU4gBqWk5t2F2o1Xr",
        refresh_token="1/E2w6hL8_GPKaMJ6A3Mem7dyK1Sfco2YrL3sKuBcInFk",
    )

    u.put()

    client = Client(redirect_uri="http://www.demo.se", name="Demo", user=u)
    client.generate_secret()
    client.put()

    return "User: " + str(u.key().id())

    #client = Client(redirect_uri="http://localhost:8080/login/", name="Moviehub")
    #client.generate_secret()
    #client.put()

    #return "Added demo data"
    #for m in movies:
    #    m.put()

@app.route("/_data/add/movies")
def add_sample_data():
    from moviehub.core.models import Movie
    from moviehubapi import Moviehub

    movies = [
        Movie(title="Akira", imdb_id="tt0094625"),
        Movie(title="Oldboy", imdb_id="tt0364569"),
        Movie(title="Donnie Darko", imdb_id="tt0246578"),
        Movie(title="Memento", imdb_id="tt0209144"),
        Movie(title="The Matrix", imdb_id="tt0133093"),
        Movie(title="City of God", imdb_id="tt0317248"),
        Movie(title="Twelve Monkeys", imdb_id="tt0114746"),
        Movie(title="Infernal Arrairs", imdb_id="tt0338564"),
        Movie(title="A Clockwork Orange", imdb_id="tt0066921"),
        Movie(title="Clerks", imdb_id="tt0109445"),
        Movie(title="The Big Lebowski", imdb_id="tt0118715"),
        Movie(title="Fear and Loathing in Las Vegas", imdb_id="tt0120669"),
        Movie(title="Lock, Stock and Two Smoking Barrels", imdb_id="tt0120735"),
        Movie(title="Snatch", imdb_id="tt0208092"),
        Movie(title="RocknRolla", imdb_id="tt1032755"),
        Movie(title="Sherlock Holmes", imdb_id="tt0988045"),
        Movie(title="A Scanner Darkly", imdb_id="tt0405296"),
        Movie(title="The Fountain", imdb_id="tt0414993"),
        Movie(title="District 9", imdb_id="tt1136608"),
        Movie(title="Into the Wild", imdb_id="tt0758758"),
        Movie(title="American Psycho", imdb_id="tt0144084"),
        Movie(title="Ocean's Eleven", imdb_id="tt0240772"),
        Movie(title="Fight Club", imdb_id="tt0137523"),
        Movie(title="Se7en", imdb_id="tt0114369"),
        Movie(title="The Usual Suspects", imdb_id="tt0114814"),
        Movie(title="Cinderella Man", imdb_id="tt0352248"),
        Movie(title="The Wrestler", imdb_id="tt1125849"),
        Movie(title="Crazy Heart", imdb_id="tt1263670"),
        Movie(title="Amelie", imdb_id="tt0211915"),
        Movie(title="The Silence of the Lambs", imdb_id="tt0102926"),
        Movie(title="Red Dragon", imdb_id="tt0289765"),
        Movie(title="Star Wars", imdb_id="tt0076759"),
        Movie(title="Star Wars: Episode V - The Empire Strikes Back", imdb_id="tt0080684"),
        Movie(title="Star Wars: Episode VI - Return of the Jedi", imdb_id="tt0086190"),
        Movie(title="The Lord of the Rings: The Fellowship of the Ring ", imdb_id="tt0120737"),
        Movie(title="The Lord of the Rings: The Two Towers", imdb_id="tt0167261"),
        Movie(title="The Lord of the Rings: The Return of the King", imdb_id="tt0167260"),
        Movie(title="Pan's Labyrinth", imdb_id="tt0457430"),
        Movie(title="Taxi Driver", imdb_id="tt0075314"),
        Movie(title="Goodfellas", imdb_id="tt0099685"),
        Movie(title="L.A. Confidential", imdb_id="tt0119488"),
        Movie(title="The Hurt Locker", imdb_id="tt0887912"),
        Movie(title="(500) Days of Summer", imdb_id="tt1022603"),
        Movie(title="Garden State", imdb_id="tt0333766"),
        Movie(title="Dark City", imdb_id="tt0118929"),
        Movie(title="City of Ember", imdb_id="tt0970411"),
        Movie(title="Stardust", imdb_id="tt0486655"),
        Movie(title="The Princess Bride", imdb_id="tt0093779"),
        Movie(title="The Trueman Show", imdb_id="tt0120382"),
        Movie(title="Eternal Sunshine of the Spotless Mind", imdb_id="tt0338013"),
        Movie(title="Constantine", imdb_id="tt0360486"),
        Movie(title="The Illusionist", imdb_id="tt0443543"),
        Movie(title="The Prestige", imdb_id="tt0482571"),
        Movie(title="3 Idiots", imdb_id="tt1187043"),
        Movie(title="Raiders of the Lost Ark", imdb_id="tt0082971"),
        Movie(title="American History X", imdb_id="tt0120586"),
        Movie(title="American Beauty", imdb_id="tt0169547"),
        Movie(title="Role Models", imdb_id="tt0430922"),
        Movie(title="Office Space", imdb_id="tt0151804"),
        Movie(title="Reservoir Dogs", imdb_id="tt0105236"),
        Movie(title="Pulp Fiction", imdb_id="tt0110912"),
        Movie(title="From Dusk Till Dawn", imdb_id="tt0116367"),
        Movie(title="Heat", imdb_id="tt0113277"),
        Movie(title="The Sixth Sense", imdb_id="tt0167404"),
        Movie(title="Blade Runner", imdb_id="tt0083658"),
        Movie(title="Zodiac", imdb_id="tt0443706"),
        Movie(title="Walk The Line", imdb_id="tt0358273"),
        Movie(title="V for Vendetta", imdb_id="tt0434409"),
        Movie(title="Kiss Kiss Bang Bang", imdb_id="tt0373469"),
        Movie(title="Big Fish", imdb_id="tt0319061"),
        Movie(title="Groundhog Day", imdb_id="tt0107048"),
        Movie(title="Lost in Translation", imdb_id="tt0335266"),
        Movie(title="In Bruges", imdb_id="tt0780536"),
        Movie(title="Children of Men", imdb_id="tt0206634"),
        Movie(title="Lord of War", imdb_id="tt0399295"),
        Movie(title="Thank You for Smoking", imdb_id="tt0427944"),
        Movie(title="Full Metal Jacket", imdb_id="tt0093058"),
        Movie(title="Ip Man", imdb_id="tt1220719"),
        Movie(title="Rush Hour", imdb_id="tt0120812"),
        Movie(title="Shutter Island", imdb_id="tt1130884"),
        Movie(title="Trainspotting", imdb_id="tt0117951"),
        Movie(title="Slumdog Millionaire", imdb_id="tt1010048"),
        Movie(title="The 51st State", imdb_id="tt0227984"),
        Movie(title="28 Days Later...", imdb_id="tt0289043"),
        Movie(title="Sin City", imdb_id="tt0401792"),
        Movie(title="Crouching Tiger, Hidden Dragon ", imdb_id="tt0190332"),
        Movie(title="Dogma", imdb_id="tt0120655"),
        Movie(title="The Fighter", imdb_id="tt0964517"),
        Movie(title="Half Nelson", imdb_id="tt0468489"),
        Movie(title="Boyz n the Hood", imdb_id="tt0101507"),
        Movie(title="South Park: Bigger Longer & Uncut", imdb_id="tt0158983"),
        Movie(title="Crank", imdb_id="tt0479884"),
        Movie(title="A Beautiful Mind", imdb_id="tt0268978"),
        Movie(title="Forest Gump", imdb_id="tt0109830"),
        Movie(title="Almost Famous", imdb_id="tt0181875"),
        Movie(title="Tropic Thunder", imdb_id="tt0942385"),
        Movie(title="Catch Me If You Can", imdb_id="tt0264464"),
        Movie(title="Crash", imdb_id="tt0375679"),
        Movie(title="Avatar", imdb_id="tt0499549"),
        Movie(title="The Smurfs", imdb_id="tt0472181"),

    ]

    #for m in movies:
        #m.put()

    p = Moviehub(client_id="1", client_secret="1", access_token="abc");
    p.add_recommendation_review(movies=movies[0].id()+","+movies[1].id(), body="test", rating=70)
