# -*- coding: utf-8 -*-

import json
from google.appengine.api import urlfetch
from flask.globals import g

from oauth2client.client import FlowExchangeError

from flask import request, redirect, session
from moviehub.api import api
from moviehub.api.utils import get_error_response, json_result
from moviehub.core.models import Client, User, AuthToken, AuthCode

@api.route("/api/info/")
@api.require_client
def client_info():
    client = g.api_client

    return json_result(json.dumps(client.to_dict()))

# TODO: add control if the user is authenticated and if he is,
# this scenarios can happen with response_type==code:
# - if user have allowed the client before:
#       redirect back to redirect_uri with code as a parameter
#   else, ask the user if he wants to accept the client to allow read and
#       write access for his account to the 3rd party client.
#       if true, redirect back to redirect_uri with code as a parameter
#       if false, redirect back with an error response
#
# this scenarios can happen with response_type==token
# - if the code is valid and within timeframe (10 seconds or less??)
#       return a new unique token
# - if the code is invalid
#       return error response

@api.route("/api/session/")
def get_session():
    if "user_id" in session:
        session.pop("user_id", None)
    return "removed sessions"

@api.route("/api/s/")
def set_session():
    session["user_id"] = int(request.args.get("user_id"))

    return "hej %s" % session["user_id"]

@api.route("/api/auth/", methods=["GET", "POST"])
def auth_request():
    if request.args.get("response_type") == "code":
        client_id = request.args.get("client_id", None)
        if not client_id:
            return get_error_response(
                message="Missing required parameter: client_id",
                status_code=400 # bad request
            )
        client_id = int(client_id)
        client = Client.get_by_id(client_id)
        if client: #and client.redirect_uri == request.args.get("redirect_uri", None):
            session["client_id"] = client.key().id()
            # TODO: check if user is logged in or send redirect to Google OAuth 2.0 login
            if not "user_id" in session:
                return redirect(api.google_oauth.step1_get_authorize_url(redirect_uri="https://movie-hub.appspot.com/oauth2callback/") + "&state=" + str(client.key().id()))
            else:
                # when user have logged in via google oauth2, we should ask the user if it want to allow
                # this client unless the client is "trusted"
                if client.trusted:
                    user = User.get_by_id(session["user_id"])
                    code = AuthCode.generate_code(user, client)
                    return redirect(client.redirect_uri + "?code=%s" % code.code)
                else:
                    # render view and ask...
                    return "Untrusted clients aren't implemented yet"
        else:
            return "No Client!"
    # try to return a token to the client, if the token request is valid
    elif request.method == "POST" and request.args.get("response_type") == "token":
        client_id = request.args.get("client_id", None)
        if not client_id:
            return get_error_response(
                message="Missing required parameter: client_id",
                status_code=400 # bad request
            )
        client = Client.get_by_id(int(client_id))
        if not client:
            return get_error_response(
                message="Unknown client_id",
                status_code=400 # bad request
            )
        if client.secret == request.args.get("client_secret"):
            # secret is correct, check code and genrate new token and delete the code.
            code = AuthCode.gql("WHERE code = :1", request.args.get("code", "")).get()
            if code:
                token = AuthToken.generate_token(code.user, code.client)
                token.put()
                code.delete()
                return token.token
            return get_error_response(
                message="code does not exist",
                status_code=400 # bad request
            )

    return get_error_response(
        message="Missing required parameter: response_type",
        status_code=400 # bad request
    )

@api.route("/oauth2callback/")
def request_token():
    #try: # try to redeem an access token
    if "code" in request.args:
        try:
            cred = api.google_oauth.step2_exchange(request.args.get("code"))
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
        return redirect("/api/auth/?response_type=code&client_id=" + request.args.get("state"))

    else: # probably error return... may fix this later.
        return "Could not get access token :)"