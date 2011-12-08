# -*- coding: utf-8 -*-

from flask import request
from moviehub.api import api
from moviehub.api.utils import get_error_response
from moviehub.core.models import Client

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
        if client and client.redirect_uri == request.args.get("redirect_uri", None):
            return "The client and redirect_uri matched!"
        #else:
        #    return "Something else"

        return "Client id=%s" % (client_id)
    # try to return a token to the client, if the token request is valid
    elif request.args.get("response_type") == "token":
        return "No token implementation yet :)"
    return get_error_response(
        message="Missing required parameter: response_type",
        type=400 # bad request
    )
