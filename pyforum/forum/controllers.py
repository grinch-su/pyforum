from flask import render_template, abort, redirect, url_for

from pyforum.forum import forum
from pyforum.forum.forms import NewTaskForm
from pyforum.forum.models import Topic, Category, Post, Tag


@forum.route('/', methods=['GET'])
def topics():
    return render_template('forum/topics.html', title='Обсуждения')


@forum.route('topic/new', methods=['GET', 'POST'])
def create_topic():
    form = NewTaskForm()
    if form.validate_on_submit():
        return redirect(url_for('forum.topics'))
    return render_template('forum/create_topic.html', title='Создание нового обсуждения', form = form)


@forum.route('topic/<topic_id>', methods=['GET', 'POST'])
def topic(topic_id):
    subject = None
    if subject == None:
        abort(404)
    return render_template('forum/topic.html')
