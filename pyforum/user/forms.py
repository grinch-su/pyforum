from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import EmailField
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_babel import lazy_gettext

class SignUpForm(FlaskForm):
    username = StringField(lazy_gettext(u'Имя пользователя:'), validators=[InputRequired(lazy_gettext(u'Введите имя пользоватля!'))])
    email = EmailField(lazy_gettext(u'Эл. адрес:'), validators=[InputRequired(lazy_gettext(u'Введите эл. адрес!'))])
    password = PasswordField(lazy_gettext(u'Пароль:'),  validators=[InputRequired(lazy_gettext(u'Введите пароль!')),
                                                           EqualTo('confirm', message=lazy_gettext(u'Пароли должны совпадать!'))])
    confirm = PasswordField(lazy_gettext(u'Повторите пароль:'))
    re_captcha = RecaptchaField()
    submit = SubmitField(lazy_gettext(u'Зарегистрироваться'))


class SignInForm(FlaskForm):
    email = EmailField(lazy_gettext(u'Ваш эл. адрес:'), validators=[InputRequired(lazy_gettext(u'Введите эл. адрес!'))])
    password = PasswordField(lazy_gettext(u'Пароль:'), validators=[InputRequired(lazy_gettext(u'Введите пароль!'))])
    re_captcha = RecaptchaField()
    submit = SubmitField(lazy_gettext(u'Авторизоваться'))


class ResetEmailForm(FlaskForm):
    email = EmailField(lazy_gettext(u'Эл. адрес'), validators=[InputRequired(lazy_gettext(u'Введите эл. адрес!'))])
    submit = SubmitField(lazy_gettext(u'Сбросить пароль'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(lazy_gettext(u'Пароль:'),  validators=[InputRequired(lazy_gettext(u'Введите пароль!')),
                                                           EqualTo('confirm', message=lazy_gettext(u'Пароли должны совпадать!'))])
    confirm = PasswordField(lazy_gettext(u'Повторите пароль:'))
    submit = SubmitField(lazy_gettext(u'Изменить пароль'))
