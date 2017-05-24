from os import environ

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

# configuration app
# example: export APP_SETTINGS="config.DevelopmentConfig"
app.config.from_object(environ['APP_SETTINGS'])

### extensions for flask ###
# Database
db = SQLAlchemy(app)
# Auth
login_manager = LoginManager(app)
# Mail
mail = Mail(app)

# debugging
if app.debug:
    try:
        from flask_debugtoolbar import DebugToolbarExtension

        toolbar = DebugToolbarExtension(app)
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
