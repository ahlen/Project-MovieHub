# -*- coding: utf-8 -*-
from flask import Blueprint

frontend = Blueprint("frontend", __name__, template_folder="templates")

import views
