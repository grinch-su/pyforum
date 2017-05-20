from datetime import datetime

from flask_login import UserMixin

from pyforum import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)
    birth_day = db.Column(db.DateTime)
    gender = db.Column(db.String(20))
    web_site = db.Column(db.String(150))
    location = db.Column(db.String(100))
    signature = db.Column(db.String(500))
    avatar = db.Column(db.String)
    activated = db.Column(db.Boolean, default=False)

    theme = db.Column(db.String)
    language = db.Column(db.String, default='en')

    post_count = db.Column(db.Integer, default=0)
    topic_count = db.Column(db.Integer, default=0)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {} {} {}>'.format(self.username, self.email, self.password)


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    # group types
    banned = db.Column(db.Boolean, default=False, nullable=False)
    guest = db.Column(db.Boolean, default=False, nullable=False)
    user = db.Column(db.Boolean, default=False, nullable=False)
    moderator = db.Column(db.Boolean, default=False, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Group {}>'.format(self.name)
