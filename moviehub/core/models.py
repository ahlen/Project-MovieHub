# -*- coding: utf-8 -*-

import datetime

from google.appengine.ext import db

class User(db.Model):
    email = db.EmailProperty(required=True)
    google_id = db.StringProperty(required=True)
    full_name = db.StringProperty()
    # google outh2 data.
    access_token = db.StringProperty()
    token_expiry = db.DateTimeProperty()
    refresh_token = db.StringProperty()
    photo_url = db.LinkProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

    # we may implement roles so we can have users that are super users
    # in the system for eventually administration ui
    # roles = db.StringListProperty(choices=set("superuser", "user"))

class Client(db.Model):
    name = db.StringProperty(required=True)
    secret = db.StringProperty(required=True)
    redirect_uri = db.StringProperty(required=True) #db.LinkProperty()
    created_at = db.DateTimeProperty(default=datetime.datetime.utcnow)
    user = db.ReferenceProperty(User, collection_name="clients")

    def _generate_secret(self):
        return None

class TestArticle(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    def to_dict(self):
        return dict(
            id=self.key().id(),
            title=self.title,
            content=self.content,
            created_at=self.created_at.isoformat()
        )

class Movie(db.Model):
    # TODO: add model properties
    def __init__(self, id, title, imdb_id):
        self.id = id
        self.title = title
        self.imdb_id = imdb_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "imdb_id": self.imdb_id,
        }

#class Review(db.Model):
#    author = db.ReferenceProperty(User)
#    rating = db.RatingProperty()

#class Discussion(db.Model):
