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
    trust_score = db.FloatProperty(default=1.0)

    # we may implement roles so we can have users that are super users
    # in the system for eventually administration ui
    # roles = db.StringListProperty(choices=set("superuser", "user"))

    def to_dict(self):
        return dict(
            id=self.key().id(),
            full_name=self.full_name,
            photo_url=self.photo_url
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

    def to_dict(self):
        return dict(
            id=self.key().id(),
            name=self.name,
            redirect_uri=self.redirect_uri
        )

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
    likes = db.ListProperty(db.Key)

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

            if tmdb_data:
                movie.update(
                    image_url=tmdb_data.get("image_url", ""),
                    description=tmdb_data.get("description", "")
                )
            else:
                movie.update(
                    image_url="",
                    description=""
                )
        return movie

class Recommendation(db.Model):
    movies = db.ListProperty(db.Key)
    left = db.ReferenceProperty(Movie, collection_name="_left_recommendations")
    right = db.ReferenceProperty(Movie, collection_name="_right_recommendations")
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    reason_count = db.IntegerProperty(default=0)

    # reason denormalized properties
    rating = db.RatingProperty()
    upvotes_count = db.IntegerProperty(default=0)
    body = db.TextProperty()
    author = db.ReferenceProperty(User, collection_name="recommendations")
    current_reason = db.ReferenceProperty() # should always be RecommendationReason

    def top_reasons(self, *args, **kwargs):
        limit = max(min(kwargs.get("limit", 10), 10), 1)

        return RecommendationReason.all().filter("recommendation=", self.key()).order("score").fetch(limit=limit)

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
                upvotes_count=self.upvotes_count,
                body=self.body,
                created_at=self.created_at.isoformat(),
                updated_at=self.updated_at.isoformat()
            )

        if kwargs.get("include_top_reasons", False):
            reasons_count = max(min(kwargs.get("reasons_count", 10), 1))
            recommendation.update(
                reasons=self.top_reasons(limit=reasons_count)
            )

        return recommendation

class RecommendationReason(db.Model):
    recommendation = db.ReferenceProperty(Recommendation, required=True)
    author = db.ReferenceProperty(User, collection_name="recommendation_reasons", required=True)
    rating = db.RatingProperty(required=True)
    score = db.FloatProperty(default=0.0)
    upvotes_count = db.IntegerProperty(default=0)
    body = db.TextProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

    def to_dict(self, *args, **kwargs):
        reason = dict(
            id=self.key().id(),
            author=self.author.to_dict(),
            rating=self.rating,
            body=self.body,
            score=self.score,
            upvotes_count=self.upvotes_count,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
        )
        if kwargs.get("include_recommendation", False):
            reason.update(
                recommendation=self.recommendation.to_dict()
            )
        else:
            reason.update(
                recommendation=self.recommendation.to_dict(only_id=True)
            )

        return reason

class ReasonVote(db.Model):
    """
    Reason vote is used to up- or downvote a recommendation reason

    when used set parent to the RecommendationReason instance
    """

    UPVOTE=1
    DOWNVOTE=-1

    author = db.ReferenceProperty(User, collection_name="votes")
    vote = db.FloatProperty(default=0.0)

    @classmethod
    def get_vote(cls, user, parent):
        return ReasonVote.gql("WHERE ancestor is :1 and author = :2", parent, user).get()

    @classmethod
    def make_vote(cls, vote, user, parent):
        def vote_in_tx():
            v = cls.get_vote(user, parent)
            if not v:
                v = ReasonVote(author=user, parent=parent)
            else:
                parent.score += -(v.vote) # reset old vote
                if v.vote >= 1:
                    # if upvote we decrease the upvotes_count
                    parent.upvotes_count += 1

            if vote == -1:
                v.vote = cls.DOWNVOTE * user.trust_score
            elif vote == 1:
                parent.upvotes_count += 1
                v.vote = cls.UPVOTE * user.trust_score
            else:
                return

            parent.score += float(v.vote)
            db.put([parent, v]) # save both parent and reason

            return v
        vote = db.run_in_transaction(vote_in_tx)

        return vote

    @classmethod
    def delete_vote(cls, user, parent):
        def delete_in_tx():
            vote = cls.get_vote(user, parent)
            if not vote:
                return False # return false if no vote exists

            parent.score += -(vote.vote)
            parent.upvotes_count -= 1
            vote.delete()
            parent.put()

            return True
        return db.run_in_transaction(delete_in_tx)

    def to_dict(self, *args, **kwargs):
        if self.vote >= 1:
            vote_type = "upvote"
        else:
            vote_type = "downvote"

        return dict(
            recommendation_reason=self.parent().to_dict(),
            author=self.author.to_dict(),
            vote=vote_type
        )