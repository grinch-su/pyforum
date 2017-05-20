import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Flask
    DEBUG = False
    TESTING = False
    SECRET_KEY = ''
    CSRF_ENABLED = True
    # SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = (environ['DATABASE_URL'])
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:8497@localhost/forum"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # reCAPTCHA
    RECAPTCHA_PUBLIC_KEY = '6LfM0CEUAAAAALbGsC_3zUk0-A9Hx2zWip1CVVe6'
    RECAPTCHA_PRIVATE_KEY = '6LfM0CEUAAAAAC8uRKYCbgsQscMkbgvIfiFcj2pB'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = '\xeaX\xc2\xef\xfc\xbc\x88Hq\x9a\x81\x9d\x04\xf3d]E4\xe2B\x7f\xf3\xd1l'
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = '\x05\xac!\xf68\xda\x1a\x8fE\x8c\xfemoN#O\xeccQ\xae\xe8+\xab\x16'


config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig
}
