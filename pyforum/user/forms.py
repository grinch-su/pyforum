from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import EmailField
from wtforms import SubmitField, StringField, PasswordField


class SignUpForm(FlaskForm):
    username = StringField(label='Имя пользователя:')
    email = EmailField(label='Эл. адрес:')
    password = PasswordField(label='Пароль:')
    confirm = PasswordField(label='Повторите пароль:')
    recaptcha = RecaptchaField()
    submit = SubmitField('Зарегистрироваться')


class SignInForm(FlaskForm):
    email = EmailField(label='Ващ эл. адрес:')
    password = PasswordField(label='Пароль:')
    submit = SubmitField('Авторизоваться')


class ForgotPasswordForm(FlaskForm):
    email = EmailField(label='Эл. адрес')
    submit = SubmitField('Сбросить пароль')
