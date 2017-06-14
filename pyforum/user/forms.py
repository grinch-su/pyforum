"""
user module
"""

from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import EmailField
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_babel import lazy_gettext

class SignUpForm(FlaskForm):
    # форма для регистрациии
    username = StringField(validators=[InputRequired(lazy_gettext(u'Введите имя пользоватля!'))])
    email = EmailField(validators=[InputRequired(lazy_gettext(u'Введите эл. адрес!'))])
    password = PasswordField(validators=[InputRequired(lazy_gettext(u'Введите пароль!')),
                                                           EqualTo('confirm', message=lazy_gettext(u'Пароли должны совпадать!'))])
    confirm = PasswordField()
    re_captcha = RecaptchaField()
    submit = SubmitField()


class SignInForm(FlaskForm):
    # форма для авторизации
    email = EmailField(validators=[InputRequired(lazy_gettext(u'Введите эл. адрес!'))])
    password = PasswordField(validators=[InputRequired(lazy_gettext(u'Введите пароль!'))])
    re_captcha = RecaptchaField()
    submit = SubmitField()


class ResetEmailForm(FlaskForm):
    # форма для восстановления аккаунта
    email = EmailField(validators=[InputRequired(lazy_gettext(u'Введите эл. адрес!'))])
    submit = SubmitField()


class ResetPasswordForm(FlaskForm):
    # форма для восстановления пароля
    password = PasswordField(validators=[InputRequired(lazy_gettext(u'Введите пароль!')),
                                                           EqualTo('confirm', message=lazy_gettext(u'Пароли должны совпадать!'))])
    confirm = PasswordField()
    submit = SubmitField()
