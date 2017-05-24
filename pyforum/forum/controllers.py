from flask import render_template, abort, redirect, url_for, request, flash, g
from flask_login import  login_required

from pyforum import db
from pyforum.forum import forum
from pyforum.forum.forms import NewTaskForm, NewPostForm
from pyforum.forum.models import Topic, Category, Post, Tag


@forum.route('/', methods=['GET'])
def topics():
    topics = Topic.query.all()
    return render_template('forum/topics.html',
                           title='Обсуждения',
                           topics = topics
                           )


@forum.route('topic/new', methods=['GET', 'POST'])
@login_required
def create_topic():
    form = NewTaskForm()
    if request.method == 'POST':
        if not form.title.data:
            flash('Необходимо указать загаловок','error')
        elif not form.content.data:
            flash('Необходимо указать содержание', 'error')
        else:
            task = Topic(title=form.title.data,
                         content=form.content.data
                         )
            task.user_id = g.user.id
            db.session.add(task)
            db.session.commit()
            flash('Обсуждение было создано успешно')
        return redirect(url_for('forum.topics'))
    return render_template('forum/create_topic.html', title='Создание нового обсуждения', form = form)


@forum.route('topic/<int:topic_id>', methods=['GET', 'POST'])
def topic(topic_id):
    topic_item = Topic.query.get(topic_id)
    form = NewPostForm()
    if request.method == 'GET':
        return render_template('forum/topic.html',form = form, topic = topic_item)
    if request.method == 'POST':
        post = Post(
            content=form.content.data
        )
        post.user_id = g.user.id
        db.session.add(post)
        db.session.commit()
        flash('Ответ отправлен')
        return redirect(url_for('forum.topic',topic_id=topic_item.id))
    if topic_item.id == g.user.id:
        # edit topic
        db.session.commit()
        return redirect(url_for('forum.topics'))
    flash('У вас нет прав редактировать это обсуждение', 'error')
    return redirect(url_for('topic', topic_id=topic_id))