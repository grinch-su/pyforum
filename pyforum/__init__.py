from os import environ

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel

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
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension(app)
    except:
        pass

# import modules
from pyforum.general import general as general_module
from pyforum.user import user as user_module
from pyforum.forum import forum as forum_module
from  pyforum.admin import admin as admin_module

# registration blueprints
app.register_blueprint(general_module)
app.register_blueprint(user_module)
app.register_blueprint(forum_module)
app.register_blueprint(admin_module)