# -*- coding: utf-8 -*-

import datetime

class User(object):
    def __init__(self, id, full_name, photo_url):
        self.id = id
        self.full_name = full_name
        self.photo_url = photo_url

    @classmethod
    def from_dict(cls, data):
        return User(
            id=data.get("id"),
            full_name=data.get("full_name"),
            photo_url=data.get("photo_url")
        )

class Client(object):
    def __init__(self, id, name, redirect_uri):
        self.id = id
        self.name = name
        self.redirect_uri

    @classmethod
    def from_dict(cls, data):
        return Client(
            id=data.get("id"),
            name=data.get("name"),
            redirect_uri=data.get("redirect_uri")
        )

class Movie(object):
    def __init__(self, id, title, imdb_id, image_url=None, description=None):
        self.id = id
        self.title = title
        self.imdb_id = imdb_id
        self.image_url = image_url
        self.description = description

    @classmethod
    def from_dict(cls, data):
        return Movie(
            data.get("id"),
            data.get("title"),
            data.get("imdb_id"),
            data.get("image_url"),
            data.get("description")
        )

class Recommendation(object):
    def __init__(self, id, author, rating, movies, body, upvotes_count):
        self.id = id
        self.author = author
        self.rating = rating
        self.movies = movies
        self.body = body
        self.upvotes_count = upvotes_count

    @classmethod
    def from_dict(cls, data):
        if len(data)==1 and "id" in data:
            return Recommendation(
                id=data.get("id"),
                author=None,
                rating=None,
                movies=None,
                body=None,
                upvotes_count=None,
            )

        return Recommendation(
            id=data.get("id"),
            author=User.from_dict(data.get("author")),
            rating=int(data.get("rating")),
            movies=[Movie.from_dict(movie) for movie in data.get("movies")],
            body=data.get("body"),
            upvotes_count=data.get("upvotes_count"),
        )

class Reason(object):
    def __init__(self, id, recommendation, author, body, upvotes_count, created_at, updated_at):
        self.id = id
        self.recommendation = recommendation
        self.author = author
        self.body = body
        self.upvotes_count = int(upvotes_count)
        self.created_at = datetime.datetime.strptime(created_at[0:19], "%Y-%m-%dT%H:%M:%S")
        self.updated_at = datetime.datetime.strptime(updated_at[0:19], "%Y-%m-%dT%H:%M:%S")

    @classmethod
    def from_dict(cls, data):
        return Reason(
            id=data.get("id"),
            recommendation=Recommendation.from_dict(data.get("recommendation")),
            author=User.from_dict(data.get("author")),
            body=data.get("body"),
            upvotes_count=data.get("upvotes_count"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )