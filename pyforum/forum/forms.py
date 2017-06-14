"""
forum module
"""
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import InputRequired, DataRequired
from flaskckeditor import CKEditor
from flask_babel import _

class NewTaskForm(FlaskForm, CKEditor):
    # форма для создание нового обсуждения
    title = StringField(validators=[InputRequired(_('Введите заголовок!'))])
    content = TextAreaField(validators=[DataRequired(_('Введите вопрос'))])
    submit = SubmitField()


class NewPostForm(FlaskForm, CKEditor):
    # форма для создаваниея нового ответа
    content = TextAreaField(validators=[DataRequired(_('Введите ответ!'))])
    submit = SubmitField()


class NewCategoryForm(FlaskForm):
    # форма для создания новой категории
    name = StringField(validators=[InputRequired(_('Введите название!'))])
    description = TextAreaField(validators=[DataRequired(_('Введите описание!'))])
    submit = SubmitField()

class EditTopicForm(FlaskForm):
    # форма для редактирования обсуждения
    title = StringField(validators=[InputRequired(_('Введите заголовок!'))])
    content = TextAreaField(validators=[DataRequired(_('Введите содержание!'))])
    submit = SubmitField()
