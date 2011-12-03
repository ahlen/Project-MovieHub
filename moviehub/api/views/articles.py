# -*- coding: utf-8 -*-

from flask import request, Response, make_response
import json

from moviehub.api import api # import our blueprint
from moviehub.core.models import TestArticle
from moviehub.api.utils import get_error_response

@api.route("/api/articles/", methods=["POST"])
def add_article():
    article = TestArticle(
        title=request.form.get("title"),
        content=request.form.get("content")
    )
    article.put()

    return json.dumps(
        article.to_dict()
        #{"id": 100, "title": request.form["title"], "content": "shorted..."}
    )

@api.route("/api/articles/", methods=["GET"])
def articles():
    articles = TestArticle.all()
    articles_data = []
    for article in articles:
        articles_data.append(article.to_dict())

    return json.dumps(articles_data)

@api.route("/api/articles/<int:id>/")
def get_article(id):
    article = TestArticle.get_by_id(id)
    return json.dumps(article.to_dict())