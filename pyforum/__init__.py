from os import environ

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, g, flash, url_for, redirect
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension


toolbar = DebugToolbarExtension()
babel = Babel()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

app = Flask(__name__)

# configuration app
# example: export APP_SETTINGS="config.DevelopmentConfig"
app.config.from_object(environ['APP_SETTINGS'])

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'user.log_in'


mail.init_app(app)

babel.init_app(app)

if app.debug:
    try:
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
