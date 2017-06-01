from threading import Thread

from pyforum import app, mail
from flask_mail import Message


def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()