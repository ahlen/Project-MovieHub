# -*- coding: utf-8 -*-

from flask import request, Response, make_response
import json

from moviehub.api import api # import our blueprint
from moviehub.core.models import Review
from moviehub.api.utils import get_error_response

@api.route("/api/reviews/", methods=["POST"])
def add_review():
    review = Review(
        title=request.form.get("title"),
        text=request.form.get("text"),
        rating=request.form.get("rating"),
    )
    review.put()

    return json.dumps(
        review.to_dict()
        #{"id": 100, "title": request.form["title"], "content": "shorted..."}
    )

@api.route("/api/reviews/", methods=["GET"])
def reviews():
    reviews = Review.all()
    reviews_data = []
    for review in reviews:
        reviews_data.append(review.to_dict())

    return json.dumps(reviews_data)

@api.route("/api/reviews/<int:id>/")
def get_review(id):
    review = Review.get_by_id(id)
    return json.dumps(review.to_dict())