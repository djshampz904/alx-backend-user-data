#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class
    """
    pass
