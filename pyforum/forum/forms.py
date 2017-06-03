from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField
from flaskckeditor import CKEditor
from flask_babel import _

class NewTaskForm(FlaskForm, CKEditor):
    title = StringField()
    content = TextAreaField()
    submit = SubmitField(_('Создать'))


class NewPostForm(FlaskForm, CKEditor):
    content = TextAreaField()
    submit = SubmitField(_('Ответить'))
