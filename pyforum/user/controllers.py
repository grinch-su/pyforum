from datetime import datetime

from flask import render_template, redirect, url_for, Response, jsonify, flash, request, g, current_app, abort
from flask_login import logout_user, login_required, login_user, current_user

from pyforum import db, login_manager
from pyforum.user import user
from pyforum.user.models import User, Group
from pyforum.forum.models import Topic, Post
from pyforum.user.forms import SignUpForm, SignInForm, ForgotPasswordForm


@user.route('signup', methods=['GET', 'POST'])
def sign_up():
    if g.user.is_authenticated:
        flash('Вы уже вошли в систему под ником {username}'.format(username=g.user.username), 'error')
        return redirect(url_for('forum.topics'))
    form = SignUpForm()
    if request.method == 'POST':
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        flash('Пользователь успешно зарегестрирован')
        print(user)
        return redirect(url_for('forum.topics'))

    return render_template('user/sign_up.html', form=form)


@user.route('login', methods=['GET', 'POST'])
def log_in():
    if g.user.is_authenticated:
        flash('Вы уже вошли в систему под ником ' + g.user.username + '', 'error')
        return redirect(url_for('forum.topics'))
    form = SignInForm()
    forgot_form = ForgotPasswordForm()
    if request.method == 'POST':
        email = form.email.data,
        password = form.password.data
        registered_user = User.query.filter_by(email=email, password=password).first()
        if registered_user is None:
            flash('Неверное имя пользователя или пароль', 'error')
            return redirect(url_for('user.log_in'))
        else:
            login_user(registered_user)
            user = User.query.get(current_user.id)
            user.last_visit = datetime.utcnow()
            db.session.commit()
            flash('Вы успешно вошли в систему')
            return redirect(url_for('forum.topics'))

    return render_template('user/log_in.html',
                           form=form,
                           forgot_form=forgot_form,
                           title='Авторизация')


@user.route('logout', methods=['GET'])
@login_required
def log_out():
    logout_user()
    flash('Вы успешно вышли из системы')
    return redirect(url_for('forum.topics'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Неразрешенный')
    return redirect(url_for(log_in))


@user.before_request
def before_request():
    g.user = current_user


@user.route('profile/<int:user_id>', methods=['GET', 'POST'])
def show_profile_user(user_id):
    user_item = User.query.get(user_id)
    topics  = Topic.query.filter(Topic.user_id == user_id).all()
    posts = Post.query.filter(Post.user_id == user_id).all()
    if user_item.id == g.user.id:
        return render_template('user/profile.html',
                               title='Профиль пользователя - ',
                               user=user_item,
                               topics = topics,
                               posts = posts)
    elif user_item.id != g.user.id:
        return render_template('user/profile.html',
                               title='Профиль пользователя - ',
                               user=user_item,
                               topics = topics)


@user.route('members', methods=['GET'])
def members():
    members = User.query.all()
    return render_template('user/members.html', members=members)


@user.route('admin', methods=['GET', 'POST'])
def admin():
    return render_template('user/admin.html')
