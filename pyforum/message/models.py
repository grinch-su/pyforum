from datetime import datetime

from pyforum import db


class Dialog(db.Model):
    __tablename__='dialog'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Integer, default=datetime.utcnow)

    def __init__(self, ):
        pass

    def __repr__(self):
        return '<  >'.format()


class Message(db.Model):
    __tablename__='message'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.Integer, default=datetime.utcnow)
    dialog_id = db.Column(db.Integer, db.ForeignKey('dialogs.id'), nullable=False)

    def __init__(self, ):
        pass

    def __repr__(self):
        pass
