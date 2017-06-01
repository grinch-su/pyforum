from hashlib import md5
from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin

from pyforum import db


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_visit = db.Column(db.DateTime)
    birth_day = db.Column(db.DateTime)
    web_site = db.Column(db.String(100))
    signature = db.Column(db.Text)
    activated = db.Column(db.Boolean, default=False)
    status = db.Column(db.String)
    online_status = db.Column(db.Boolean, default=False)

    admin = db.Column(db.Boolean, default=False)

    tags = db.relationship('Tag', backref='user', lazy='dynamic')
    replies = db.relationship('Reply', backref='user', lazy='dynamic')
    topics = db.relationship('Topic', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User Username - {}, email - {}, password - {}, joined - {}>'.format(
            self.username,
            self.email,
            self.password,
            self.date_joined
        )

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = 0
        self.username = 'Guest'
        self.admin = False