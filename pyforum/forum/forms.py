from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from flaskckeditor import CKEditor

class NewTaskForm(FlaskForm, CKEditor):
    title = StringField()
    content = TextAreaField()
    submit = SubmitField('Создать')

class NewPostForm(FlaskForm, CKEditor):
    content = TextAreaField()
    submit = SubmitField('Ответить')