# -*- coding: utf-8 -*-

import json
from google.appengine.api import urlfetch
from flask.globals import g

from oauth2client.client import FlowExchangeError

from flask import request, redirect, session
from moviehub.api import api
from moviehub.api.utils import get_error_response, json_result
from moviehub.core.models import Client, User

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

@api.route("/api/auth/")
def auth():
    if request.args.get("response_type") == "code":
        client_id = request.args.get("client_id", None)
        if not client_id:
            return get_error_response(
                message="Missing required parameter: client_id",
                status_code=400 # bad request
            )
        client = Client.get_by_id(int(client_id))
        if client: #and client.redirect_uri == request.args.get("redirect_uri", None):
            return "The client found"
            # TODO: check if user is logged in or send redirect to Google OAuth 2.0 login

        return "Client id=%s" % (client_id)
    # try to return a token to the client, if the token request is valid
    elif request.args.get("response_type") == "token":
        return "No token implementation yet :)"
    return get_error_response(
        message="Missing required parameter: response_type",
        type=400 # bad request
    )

@api.route("/oauth2callback")
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
        return redirect("/")

    else: # probably error return... may fix this later.
        return "Could not get access token :)"