"""
forum module
"""
from flask import Blueprint
forum = Blueprint('forum', __name__, url_prefix='/')
from . import controllers