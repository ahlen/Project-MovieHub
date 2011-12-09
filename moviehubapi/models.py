# -*- coding: utf-8 -*-

import datetime

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

class Article(object):
    def __init__(self, id, title, content, created_at):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = datetime.datetime.strptime(created_at[0:19], "%Y-%m-%dT%H:%M:%S")

    @classmethod
    def from_dict(cls, data):
        return Article(
            data.get("id"),
            data.get("title"),
            data.get("content"),
            data.get("created_at")
        )

class Review(object):
    def __init__(self, id, title, author, rating, movie, text, created_at, updated_at):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating
        self.movie = movie
        self.text = text
        self.created_at = datetime.datetime.strptime(created_at[0:19], "%Y-%m-%dT%H:%M:%S")
        self.updated_at = datetime.datetime.strptime(created_at[0:19], "%Y-%m-%dT%H:%M:%S")

    @classmethod
    def from_dict(cls, data):
        return Review(
            data.get("id"),
            data.get("title"),
            data.get("author"),
            data.get("rating"),
            data.get("movie"),
            data.get("text"),
            data.get("created_at"),
            data.get("updated_at")
        )
