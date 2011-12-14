# -*- coding: utf-8 -*-

from wtforms import Form, TextField, TextAreaField, IntegerField, validators

class RecommendationForm(Form):
    target_id = IntegerField("Movie", validators=[validators.required()])
    reason = TextAreaField("Reason", validators=[validators.required(), validators.length(min=10, max=1024)])
    rating = IntegerField("Rating", default=50, validators=[validators.required(), validators.number_range(min=0, max=100)])
