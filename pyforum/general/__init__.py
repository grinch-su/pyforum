from flask import Blueprint

general = Blueprint('general', __name__, url_prefix='/')
from . import controllers
