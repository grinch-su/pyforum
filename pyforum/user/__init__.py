from flask import Blueprint

# определение модуля User
user = Blueprint('user', __name__, url_prefix='/')
from . import controllers
