from hashlib import md5
from datetime import datetime

from flask import url_for
from flask_login import UserMixin, AnonymousUserMixin
from flask_babel import _

from pyforum import db

class User(db.Model, UserMixin):
    # ORM таблица пользователей
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    ip = db.Column(db.String)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_visit = db.Column(db.DateTime)
    birth_day = db.Column(db.Date)
    web_site = db.Column(db.String(100))
    signature = db.Column(db.Text)
    activated = db.Column(db.Boolean, default=False)
    status = db.Column(db.String)
    online_status = db.Column(db.Boolean, default=False)
    lang = db.Column(db.String, default='en')
    admin = db.Column(db.Boolean, default=False)
    banned = db.Column(db.Boolean, default=False)
    replies = db.relationship('Reply', backref='user', lazy='dynamic')
    topics = db.relationship('Topic', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def role(self):
        if self.admin:
            return _('Администратор')
        else:
            return _('Пользователь')

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'avatar': self.avatar(50),
            '_link' : url_for('user.show_profile_user', username=self.username)
        }
        return json_user

    def __repr__(self):
        return '<User Username - {}, email - {}, joined - {}>'.format(
            self.username,
            self.email,
            self.date_joined
        )

class Anonymous(AnonymousUserMixin):
    # класс с анонимным пользователей(Гость)
    def __init__(self):
        self.id = 0
        self.username = 'Guest'
        self.admin = False
        self.banned = False
        self.lang = 'en'
