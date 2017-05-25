from datetime import datetime

from pyforum import db


class ChatRoom(db.Model):
    __tablename__ = 'chat_rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_datetime = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('chat_rooms', lazy='dynamic'))

    def __init__(self, name, created_datetime, user):
        self.name = name
        self.created_datetime = created_datetime
        self.creator_id = user

    def __repr__(self):
        return '<Chatroom {} {} {}>'.format(self.name, self.creator_id, self.created_datetime)


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User',
                           backref=db.backref('chat_messages', lazy='dynamic'))
    chatroom = db.relationship('ChatRoom',
                               backref=db.backref('chat_messages', lazy='dynamic'))

    def __init__(self, user_id, chatroom_id, message, timestamp):
        self.user_id = user_id
        self.chatroom_id = chatroom_id
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return '<Message {} {}>'.format(self.message, self.timestamp)
