from datetime import datetime

from flask import render_template, abort, redirect, url_for, request, flash, g
from flask_login import login_required, current_user
from flask_babel import gettext, _

from pyforum import db
from pyforum.forum import forum
from pyforum.forum.forms import NewTaskForm, NewPostForm, NewCategoryForm, EditTopicForm
from pyforum.forum.models import Topic, Category, Reply, Tag
from pyforum.user.models import User


@forum.route('/')
def index():
    categories = Category.query.order_by(Category.name.desc()).all()
    new_topics = Topic.query.order_by(Topic.date_created.desc()).limit(4).all()
    latest_member = User.query.order_by(User.date_joined.desc()).limit(1).first()
    return render_template('forum/home.html',
                           title='PyForum',
                           categories=categories,
                           new_topics=new_topics,
                           latest_member=latest_member,
                           count_members=User.query.count(),
                           count_replies=Reply.query.count(),
                           count_topics=Topic.query.count())


@forum.route('<category_name>', methods=['GET', 'POST'])
@forum.route('<category_name>/page-<int:page>', methods=['GET', 'POST'])
def category(category_name, page=1):
    topics_per_page = 5
    category = Category.query.filter_by(name=category_name).first_or_404()
    topics = Topic.query.filter_by(category_id=category.id).paginate(page, topics_per_page, True)
    return render_template('forum/category_topics.html',
                           title=category_name,
                           topics=topics,
                           category=category)


@forum.route('<category_name>/topic-<int:topic_id>', methods=['GET','POST'])
@forum.route('<category_name>/topic-<int:topic_id>/page-<int:page>', methods=['GET', 'POST'])
def topic(category_name, topic_id, page=1):
    replies_per_page = 10
    topic_item = Topic.query.get(topic_id)
    category = Category.query.filter_by(name=category_name).first_or_404()
    tags = Tag.query.filter_by(topic_id=topic_id).all()
    replies = Reply.query.filter_by(topic_id=topic_id).order_by(Reply.date_created).paginate(page,
                                                                                             replies_per_page,
                                                                                             True)

    topic_item.views += 1
    db.session.commit()
    form = NewPostForm()

    if request.method == 'POST' and form.validate_on_submit():
        reply = Reply(content=form.content.data)
        reply.category_id = category.id
        reply.topic_id = topic_id
        reply.user_id = g.user.id
        db.session.add(reply)
        db.session.commit()
        flash(gettext('Ответ отправлен'), 'success')

        return redirect(url_for(endpoint='forum.topic',
                                category_name=category_name,
                                topic_id=topic_id, page=1))

    return render_template('forum/topic.html',
                           form=form,
                           topic=topic_item,
                           replies=replies,
                           category=category,
                           tags=tags)


@forum.route('topic/new', methods=['GET', 'POST'])
@login_required
def create_topic():
    if not current_user.is_authenticated:
        flash(gettext('Войдите в систему что-бы создать обсуждение!'), 'error')
        return redirect(url_for('forum.index'))
    form = NewTaskForm()
    categories = Category.query.order_by(Category.name.desc()).all()
    if request.method == 'POST' and form.validate_on_submit():
        topic_item = Topic(title=form.title.data,
                           content=form.content.data,
                           category_id=request.form.get('category_select'))
        topic_item.user_id = g.user.id
        db.session.add(topic_item)
        db.session.commit()
        flash(gettext('Обсуждение было создано успешно'), 'success')
        return redirect(url_for('forum.index'))
    return render_template('forum/create_topic.html', title=(gettext('Создание нового обсуждения')),
                           form=form,
                           categories=categories)


@forum.route('category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    if g.user.admin == False:
        flash(gettext('Нет доступа к созданию категорий.'), 'error')
        return redirect(url_for('forum.index'))

    form = NewCategoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_category = Category(name=form.name.data,
                                description=form.description.data)
        db.session.add(new_category)
        db.session.commit()
        flash(gettext('Категория была успешно создана'), 'success')
        return redirect(url_for('forum.index'))

    return render_template('forum/create_category.html',
                           title=(_('Создание новой категрии')),
                           form=form)


@forum.route('topic/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_topic(id):
    del_topic = Topic.query.filter_by(id=id).first_or_404()
    if current_user.admin == True or del_topic.user_id == current_user.id:
        Reply.query.filter_by(topic_id=id).delete()
        db.session.delete(del_topic)
        db.session.commit()
        if current_user.admin:
            return redirect(url_for('user.admin'))
        elif del_topic.user_id == current_user.id:
            return redirect(url_for('forum.index'))
    elif del_topic.user_id != current_user.id:
        flash(_("Нет доступа к удалению даунного обсуждения"), 'error')
        return redirect(url_for('forum.index'))


@forum.route('topic/edit-topic/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_topic(id):
    topic_item = Topic.query.filter_by(id=id).first_or_404()
    categories = Category.query.order_by(Category.name.desc()).all()
    category_item = Category.query.filter_by(id=topic_item.category_id).first_or_404()
    form = EditTopicForm()
    if current_user.admin == True or topic_item.user_id == current_user.id:
        if request.method == 'POST' and form.validate_on_submit():
            topic_item.title = form.title.data
            topic_item.content = form.content.data
            topic_item.category_id = request.form.get('category_select')
            topic_item.date_last_changes = datetime.now()
            db.session.commit()
            flash(_('Обсуждения отредактировано успешно'))
            return redirect(url_for('forum.topic',
                                    category_name=category_item.name,
                                    topic_id = id,
                                    page=1))
        else:
            return render_template('forum/edit_topic.html',
                                   form=form,
                                   topic=topic_item,
                                   categories=categories)

    elif topic_item.user_id != current_user.id:
        flash(_("Нет доступа к удалению даунного обсуждения"), 'error')
        return redirect(url_for('forum.index'))
