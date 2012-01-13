# -*- coding: utf-8 -*-


from google.appengine.ext import db
from google.appengine.ext import deferred

from moviehub.core.models import Recommendation, RecommendationReason

def update_recommendation_ranking(reason_key):
    # execute the computation without to block the caller.
    deferred.defer(_update_recommendation_ranking_task, reason_key)

def _update_recommendation_ranking_task(reason_key):
    reason = RecommendationReason.get(reason_key)
    recommendation = reason.recommendation

    top_reason = RecommendationReason.all().filter("recommendation = ", recommendation).order("-score").get()
    if not top_reason.key() == recommendation.current_reason.key():
        recommendation.current_reason = top_reason
        recommendation.rating = top_reason.rating
        recommendation.author = top_reason.author
        recommendation.upvotes_count = top_reason.upvotes_count
        recommendation.body = top_reason.body
        db.put(recommendation)