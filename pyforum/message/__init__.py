from flask import Blueprint
message = Blueprint('message', __name__, url_prefix='/')
from . import controllers
