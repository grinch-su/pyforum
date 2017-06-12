import os

class Config(object):
    # Flask
    DEBUG = False
    TESTING = False
    SECRET_KEY = ''
    CSRF_ENABLED = True
    # SQLAlchemy for db
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:8497@localhost/forum"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask-Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = 'grinchfedorov@gmail.com'

    # Flask-Login for auth
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Flask-babel for localization
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'ru': 'Russian'
    }
    BABEL_DEFAULT_LOCALE = "ru"
    BABEL_DEFAULT_TIMEZONE = "UTC"

    #  reCAPTCHA
    RECAPTCHA_PUBLIC_KEY = '6LfM0CEUAAAAALbGsC_3zUk0-A9Hx2zWip1CVVe6'
    RECAPTCHA_PRIVATE_KEY = '6LfM0CEUAAAAAC8uRKYCbgsQscMkbgvIfiFcj2pB'
    # RECAPTCHA_PARAMETERS={'hl': 'en'}

class DevelopmentConfig(Config):
    # конфиг для разработки
    DEBUG = True
    SECRET_KEY = '\xeaX\xc2\xef\xfc\xbc\x88Hq\x9a\x81\x9d\x04\xf3d]E4\xe2B\x7f\xf3\xd1l'
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    # конфиг для тестирования
    TESTING = True


class ProductionConfig(Config):
    # конфиг для production
    DEBUG = False
    SECRET_KEY = '\x05\xac!\xf68\xda\x1a\x8fE\x8c\xfemoN#O\xeccQ\xae\xe8+\xab\x16'
