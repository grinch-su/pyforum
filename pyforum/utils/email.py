from threading import Thread

from flask import url_for, render_template
from itsdangerous import URLSafeTimedSerializer

from config import Config
from pyforum import app, mail
from flask_mail import Message
from flask_babel import _


def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()

def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    confirm_url = url_for('user.confirm_email',
                  token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
                  _external=True)
    html = render_template('user/auth/email_confirmation.html',
                           confirm_url=confirm_url)
    send_email(_('Подтвердите Ваш электронный адрес'),
               [user_email],
               text_body=(_('Подтвердите адрес эл.почты')),
               html_body=html)


def send_reset_password(user_email):
    confirm_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    url = url_for('user.reset_with_token',
                  token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
                  _external=True)
    html = render_template('user/auth/email_reset.html',
                           reset_url=url)


    send_email(_('Восстановление пароля'),
               [user_email],
               text_body=(_('Восстановление пароля')),
               html_body=html)