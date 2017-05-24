from datetime import datetime

from pyforum import db


class Topic(db.Model):
    __tablename__='topics'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=200))
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime)
    date_last_changes = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    locked = db.Column(db.Boolean, default=False)
    amount = db.Column(db.Integer, default=0)


    def __init__(self, title,content):
        self.title = title
        self.content = content
        self.date_created = datetime.utcnow
        self.date_last_changes = datetime.utcnow


    def __repr__(self):
        return '<Topics {}>'.format(self.title)

class Post(db.Model):
    __tablename__='posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Posts {}>'.format(self.content)


class Category(db.Model):
    __tablename='categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Tag(db.Model):
    __tablename__='tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tags {}>'.format(self.name)
