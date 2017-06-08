from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField
from wtforms.validators import InputRequired, DataRequired
from flaskckeditor import CKEditor
from flask_babel import _

class NewTaskForm(FlaskForm, CKEditor):
    title = StringField(_('Заголовок'), validators=[InputRequired(_('Введите заголовок!'))])
    content = TextAreaField(validators=[DataRequired(_('Введите вопрос'))])
    submit = SubmitField(_('Создать'))


class NewPostForm(FlaskForm, CKEditor):
    content = TextAreaField(_('Ответ'), validators=[DataRequired(_('Введите ответ!'))])
    submit = SubmitField(_('Ответить'))


class NewCategoryForm(FlaskForm):
    name = StringField(_('Название'), validators=[InputRequired(_('Введите название!'))])
    description = TextAreaField(_('Описание'), validators=[DataRequired(_('Введите описание!'))])
    submit = SubmitField(_('Ответить'))

class EditTopicForm(FlaskForm):
    title = StringField(_('Заголовок'), validators=[InputRequired(_('Введите заголовок!'))])
    content = TextAreaField(validators=[DataRequired(_('Введите содержание!'))])
    submit = SubmitField(_('Сохранить'))
