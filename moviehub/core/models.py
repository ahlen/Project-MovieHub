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

    def to_dict(self):
        return dict(
            id=self.key().id(),
            full_name=self.full_name,
            photo_url=self.photo_url,
        )

class Client(db.Model):
    name = db.StringProperty(required=True)
    secret = db.StringProperty() #required=True
    redirect_uri = db.StringProperty(required=True) #db.LinkProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    user = db.ReferenceProperty(User, collection_name="clients")
    trusted = db.BooleanProperty(default=False)

    @classmethod
    def authenticate(cls, id, secret):
        client =  cls.get_by_id(id)
        if client and client.secret == secret:
            return client
        else:
            return None

    def generate_secret(self):
        """
        Generate secret for the client should use as the API identifier.
        """
        import hashlib
        h = hashlib.new("sha1")
        h.update("%s:%s:%s" % (self.redirect_uri, self.created_at.isoformat(), self.name))

        self.secret = h.hexdigest()

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
    title = db.StringProperty(required=True)
    imdb_id = db.StringProperty()

    def to_dict(self, *args, **kwargs):
        # if we only wants the id, just return the dict(id=...)
        if kwargs.get("only_id", False):
            return dict(
                id=self.key().id()
            )

        movie = dict(
            id=self.key().id(),
            title=self.title,
            imdb_id=self.imdb_id
        )
        if kwargs.get("include_remote", False):
            from moviehub.api import tmdb
            tmdb_data = tmdb.extract_movie_data(self.imdb_id)

            movie.update(
                image_url=tmdb_data.get("image_url", ""),
                description=tmdb_data.get("description", "")
            )
        return movie

class Review(db.Model):
    author = db.ReferenceProperty(User, collection_name="reviews")
    rating = db.RatingProperty()
    movie = db.ReferenceProperty(Movie, collection_name="reviews")
    text = db.TextProperty()
    title = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

    def to_dict(self):
        return {
            "id": self.key().id(),
            "title": self.title,
            "author": self.author,
            "rating": self.rating,
            "movie": self.movie,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


"""
class Recommendation(db.Model):
    author = db.ReferenceProperty(User, collection_name="recommendations")#, required=True)
    source = db.ReferenceProperty(Movie, collection_name="source_recommendations", required=True)
    target = db.ReferenceProperty(Movie, collection_name="target_recommendations", required=True)
    rating = db.RatingProperty(required=True)
    body = db.TextProperty(required=True)
    selected_review = db.ReferenceProperty() # should always be of type RecommendationReview

    @classmethod
    def check_uniqueness(cls, source, target):
        uniq_left = Recommendation.all().filter("source = ", source) \
            .filter("target = ", target).get()
        uniq_right = Recommendation.all().filter("source = ", target) \
            .filter("target = ", source).get()

        return not uniq_left and not uniq_right

    def to_dict(self):
        return dict(
            id=self.parent_key().id(),
            author=self.author.to_dict(),
            source=self.source.to_dict(include_remote=True),
            target=self.target.to_dict(include_remote=True),
            rating=self.rating,
            body=self.body
        )

class RecommendationPair(db.Model):
    movies = db.ListProperty(item_type=db.Key)

class RecommendationReview(db.Model):
    recommendation = db.ReferenceProperty(Recommendation)
    author = db.ReferenceProperty(User, collection_name="recommendation_reviews")
    rating = db.RatingProperty(required=True)
    body = db.TextProperty(required=True)
"""
"""
Rewrite to this model:

Recommendation have
    author
    source
    target
    rating
    body
    selected_review
    created_at

RecommendationReview have
    recommendation (reference)
    author
    rating (author chosen)
    score (users up/down vote)
    body
    created_at

RecommendationIndex have (two-way) and belongs to parent
    source
    target
    rating

    (so we can do filter(source=this).order(rating))
"""

class Recommendation(db.Model):
    author = db.ReferenceProperty(User, collection_name="recommendations")
    movies = db.ListProperty(db.Key)
    left = db.ReferenceProperty(Movie, collection_name="_left_recommendations")
    right = db.ReferenceProperty(Movie, collection_name="_right_recommendations")
    #source = db.ReferenceProperty(Movie, collection_name="source_recommendations")
    #target = db.ReferenceProperty(Movie, collection_name="target_recommendations")
    rating = db.RatingProperty()
    body = db.TextProperty()
    selected_review = db.ReferenceProperty() # should always be RecommendationReview
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

    def top_reviews(self, *args, **kwargs):
        limit = max(min(kwargs.get("limit", 10), 10), 1)

        return RecommendationReview.all().filter("recommendation=", self.key()).order("score").fetch(limit=limit)

    def to_dict(self, *args, **kwargs):
        if kwargs.get("only_id", False):
            recommendation = dict(
                id=self.key().id()
            )
        else:
            recommendation = dict(
                id=self.key().id(),
                author=self.author.to_dict(),
                movies=[movie.to_dict(include_remote=True) for movie in Movie.get(self.movies)],
                rating=self.rating,
                body=self.body,
                created_at=self.created_at.isoformat(),
                updated_at=self.updated_at.isoformat()
            )

        if kwargs.get("include_top_reviews", False):
            reviews_count = max(min(kwargs.get("reviews_count", 10), 1))
            recommendation.update(
                reviews=self.top_reviews(limit=reviews_count)
            )

        return recommendation

class RecommendationReview(db.Model):
    recommendation = db.ReferenceProperty(Recommendation, required=True)
    author = db.ReferenceProperty(User, collection_name="recommendation_reviews", required=True)
    rating = db.RatingProperty(required=True)
    score = db.FloatProperty(default=0.0)
    body = db.TextProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

    def to_dict(self, *args, **kwargs):
        review = dict(
            id=self.key().id(),
            author=self.author.to_dict(),
            rating=self.rating,
            body=self.body,
            score=self.score,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
        )
        if kwargs.get("include_recommendation", False):
            review.update(
                recommendation=self.recommendation.to_dict()
            )
        else:
            review.update(
                recommendation=self.recommendation.to_dict(only_id=True)
            )

        return review