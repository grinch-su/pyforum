from datetime import datetime

from pyforum import db


class Dialog(db.Model):
    __tablename__ = 'dialog'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Dialog {}>'.format(self.name)


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.Integer, default=datetime.utcnow)

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return '<Message {}>'.format(self.message)
