from flask import render_template, abort, redirect, url_for, request, flash, g
from flask_login import login_required, current_user
from flask_babel import gettext

from pyforum import db
from pyforum.forum import forum
from pyforum.forum.forms import NewTaskForm, NewPostForm
from pyforum.forum.models import Topic, Category, Reply, Tag
from pyforum.user.models import User


@forum.route('/')
def index():
    categories = Category.query.order_by(Category.name.desc()).all()
    new_topics = Topic.query.order_by(Topic.date_created.desc()).limit(4).all()
    latest_member = User.query.order_by(User.date_joined.desc()).limit(1).first()
    count_topics = Topic.query.count()
    count_members = User.query.count()
    count_replies = Reply.query.count()
    return render_template('forum/home.html',
                           title='PyForum',
                           categories=categories,
                           new_topics=new_topics,
                           latest_member=latest_member,
                           count_members=count_members,
                           count_replies=count_replies,
                           count_topics=count_topics)


@forum.route('<category_name>', methods=['GET', 'POST'])
@forum.route('<category_name>/page-<int:page>', methods=['GET', 'POST'])
def category(category_name, page=1):
    topics_per_page = 5
    category = Category.query.filter_by(name=category_name).first_or_404()
    topics = Topic.query.filter_by(category_id=category.id).paginate(page, topics_per_page, True)
    return render_template('forum/category_topics.html', title=category_name, topics=topics, category=category)


@forum.route('<category_name>/topic-<int:topic_id>/page-<int:page>', methods=['GET', 'POST'])
def topic(category_name, topic_id, page=1):
    replies_per_page = 10
    topic_item = Topic.query.get(topic_id)
    category = Category.query.filter_by(name=category_name).first_or_404()
    tags = Tag.query.filter_by(topic_id=topic_id).all()
    replies = Reply.query.filter_by(topic_id=topic_id).order_by(Reply.date_created).paginate(page, replies_per_page,True)

    topic_item.views += 1
    db.session.commit()
    form = NewPostForm()

    if request.method == 'POST':
        if not form.content.data:
            flash(gettext('Необходимо указать ответ'), 'error')
        else:
            reply = Reply(
                content=form.content.data
            )
            reply.category_id = category.id
            reply.topic_id = topic_id
            reply.user_id = g.user.id
            db.session.add(reply)
            db.session.commit()
            flash(gettext('Ответ отправлен'), 'success')
            return redirect(url_for('forum.topic', category_name=category_name, topic_id=topic_id, page=1))
    return render_template('forum/topic.html',
                           form=form,
                           topic=topic_item,
                           replies=replies,
                           category=category,
                           tags=tags)


@forum.route('topic/new', methods=['GET', 'POST'])
def create_topic():
    if not current_user.is_authenticated:
        flash(gettext('Войдите в систему что-бы создать обсуждение!'), 'error')
        return redirect(url_for('forum.index'))
    form = NewTaskForm()
    categories = Category.query.order_by(Category.name.desc()).all()
    if request.method == 'POST':
        if not form.title.data:
            flash(gettext('Необходимо указать загаловок'), 'error')
            return redirect(url_for('forum.create_topic'))
        elif not form.content.data:
            flash(gettext('Необходимо указать содержание'), 'error')
            return redirect(url_for('forum.create_topic'))
        else:
            topic = Topic(title=form.title.data,
                          content=form.content.data,
                          category_id=request.form.get('category_select')
                          )
            topic.user_id = g.user.id
            db.session.add(topic)
            db.session.commit()
            flash(gettext('Обсуждение было создано успешно'), 'success')
            return redirect(url_for('forum.index'))
    return render_template('forum/create_topic.html', title=(gettext('Создание нового обсуждения')),
                           form=form,
                           categories=categories)


@forum.route('category/new', methods=['GET', 'POST'])
def new_category():
    if g.user.admin == False:
        flash(gettext('Нет доступа к созданию категорий.'), 'error')
        return redirect(url_for('forum.index'))
    if request.method == 'POST':
        if not request.form.get('name'):
            flash(gettext('Введите название категории'), 'error')
        if not request.form.get('description'):
            flash(gettext('Введите опписание категории'), 'error')
        else:
            category = Category(
                name=request.form.get('name'),
                description=request.form.get('description')
            )
            db.session.add(category)
            db.session.commit()
            flash(gettext('Категория была успешно создана'), 'success')
            return redirect(url_for('forum.index'))
    return render_template('forum/create_category.html',
                           title=gettext('Создание новой категрии'))
