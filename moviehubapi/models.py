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
        return Recommendation(
            id=data.get("id"),
            author=User.from_dict(data.get("author")),
            rating=int(data.get("rating")),
            movies=[Movie.from_dict(movie) for movie in data.get("movies")],
            body=data.get("body"),
            upvotes_count=data.get("upvotes_count"),
        )

# TODO: add RecommendationReason