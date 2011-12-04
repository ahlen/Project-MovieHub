# -*- coding: utf-8 -*-
from flask import Response
import json

def get_error_response(message, type="MoviehubApiException", status_code=404):
    """
    return
    """
    response = Response(
        json.dumps({"error": { "type": type, "message": message }}),
        mimetype="application/json",
        status=status_code
    )
    return response
