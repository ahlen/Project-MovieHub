# -*- coding: utf-8 -*-
from flask import Response

def json_result(data, status_code=200):
    """
    return a result with application/json as mime-type
    """
    return Response(
        data,
        mimetype="application/json",
        status=status_code
    )
