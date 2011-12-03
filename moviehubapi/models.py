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