from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import EmailField
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_babel import _

class SignUpForm(FlaskForm):
    username = StringField(_('Имя пользователя:'), validators=[InputRequired(_('Введите имя пользоватля!'))])
    email = EmailField(_('Эл. адрес:'), validators=[InputRequired(_('Введите эл. адрес!'))])
    password = PasswordField(_('Пароль:'),  validators=[InputRequired(_('Введите пароль!')),
                                                           EqualTo('confirm', message=_('Пароли должны совпадать!'))])
    confirm = PasswordField(_('Повторите пароль:'))
    re_captcha = RecaptchaField()
    submit = SubmitField(_('Зарегистрироваться'))


class SignInForm(FlaskForm):
    email = EmailField(_('Ваш эл. адрес:'), validators=[InputRequired(_('Введите эл. адрес!'))])
    password = PasswordField(_('Пароль:'), validators=[InputRequired(_('Введите пароль!'))])
    re_captcha = RecaptchaField()
    submit = SubmitField(_('Авторизоваться'))


class ResetEmailForm(FlaskForm):
    email = EmailField(_('Эл. адрес'), validators=[InputRequired(_('Введите эл. адрес!'))])
    submit = SubmitField(_('Сбросить пароль'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_('Пароль:'),  validators=[InputRequired(_('Введите пароль!')),
                                                           EqualTo('confirm', message=_('Пароли должны совпадать!'))])
    confirm = PasswordField(_('Повторите пароль:'))
    submit = SubmitField(_('Изменить пароль'))
