from datetime import datetime

from pyforum import db


class Category(db.Model):
    __tablename = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    topics = db.relationship('Topic', backref='category', lazy='dynamic')
    replies = db.relationship('Reply', backref='category', lazy='dynamic')

    def __init__(self, name,description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Category {} {}>'.format(self.name, self.description)


class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=200))
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_last_changes = db.Column(db.DateTime)
    views = db.Column(db.Integer, default=0)
    locked = db.Column(db.Boolean, default=False)

    tags = db.relationship('Tag', backref='topic', lazy='dynamic')
    replies = db.relationship('Reply', backref='topic', lazy='dynamic')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, category_id):
        self.title = title
        self.content = content
        self.category_id = category_id

    def __repr__(self):
        return '<Topics {}>'.format(self.title)


class Reply(db.Model):
    __tablename__ = 'reply'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    date_last_changes = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Post {}>'.format(self.content)


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag {}>'.format(self.name)


# class Like(db.Model):
#     __tablename_='like'
#
#     id = db.Column(db.Integer, primary_key=True)
#
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
#
#     def __init__(self):
#         pass
