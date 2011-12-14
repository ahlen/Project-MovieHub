# -*- coding: utf-8 -*-

class MoviehubApiError(Exception):
    def __init__(self, type, message):
        Exception.__init__(self, message)
        self.type = type