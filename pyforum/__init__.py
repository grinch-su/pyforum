from os import environ

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = 0
        self.username = 'Guest'


app = Flask(__name__)

# configuration app
# example: export APP_SETTINGS="config.DevelopmentConfig"
app.config.from_object(environ['APP_SETTINGS'])

### extensions for flask ###
# Database
db = SQLAlchemy()
db.init_app(app)
# Auth
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.log_in'
login_manager.anonymous_user = Anonymous
# Mail
mail = Mail()
mail.init_app(app)
# debugging
if app.debug:
    try:
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension()
        toolbar.init_app(app)
    except:
        pass

# import modules
from pyforum.general import general as general_module
from pyforum.user import user as user_module
from pyforum.forum import forum as forum_module
from pyforum.message import message as message_module
from pyforum.chat import chat as chat_module

# registration blueprints
app.register_blueprint(general_module)
app.register_blueprint(user_module)
app.register_blueprint(forum_module)
app.register_blueprint(message_module)
app.register_blueprint(chat_module)

# create tables for db use sqlalchemy
with app.app_context():
    db.create_all()
