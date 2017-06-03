# from datetime import datetime
#
# from pyforum import db
#
#
# class ChatRoom(db.Model):
#     __tablename__ = 'chat_rooms'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=True)
#     slug = db.Column(db.String, unique=True)
#     created_datetime = db.Column(db.DateTime)
#     users = db.relationship('')
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return '<Chatroom {}>'.format(self.name)
#

# class ChatMessage(db.Model):
#     __tablename__ = 'chat_messages'
#
#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.Text)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __init__(self, message):
#         self.message = message
#
#     def __repr__(self):
#         return '<Message {}>'.format(self.message)
