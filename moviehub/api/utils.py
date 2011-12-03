# -*- coding: utf-8 -*-
from flask import Response
import json

def get_error_response(message, status_code=404):
    """
    return
    """
    response = Response(
        json.dumps({"error": { "type": "MoviehubApiException", "message": message }}),
        mimetype="application/json",
        status=status_code
    )
    return response
