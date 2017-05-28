from datetime import datetime

from flask import render_template, redirect, url_for, Response, jsonify, flash, request, g, current_app, abort
from flask_login import logout_user, login_required, login_user, current_user, AnonymousUserMixin
from flask_babel import gettext

from config import Config
from pyforum import db, login_manager, app, babel
from pyforum.user import user
from pyforum.user.models import User
from pyforum.forum.models import Topic, Reply
from pyforum.user.forms import SignUpForm, SignInForm, ForgotPasswordForm


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(Config.SUPPORTED_LANGUAGES.keys())


@babel.timezoneselector
def get_timezone():
    user = g.get('user', None)
    if user is not None:
        return user.timezone


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = 0
        self.username = 'Guest'
        self.admin = False


login_manager.login_view = 'user.log_in'
login_manager.anonymous_user = Anonymous


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash(gettext('Пожалуйста авторизируйтесь!'))
    return redirect(url_for('user.log_in'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_visit = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@user.route('signup', methods=['GET', 'POST'])
def sign_up():
    if g.user.is_authenticated:
        flash(gettext('Вы уже вошли в систему под ником {username}').format(username=g.user.username), 'error')
        return redirect(url_for('forum.index'))
    form = SignUpForm()
    if request.method == 'POST':
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data
                        )
        db.session.add(new_user)
        db.session.commit()
        flash(gettext('Пользователь успешно зарегестрирован'))
        return redirect(url_for('forum.index'))

    return render_template('user/sign_up.html', form=form)


@user.route('login', methods=['GET', 'POST'])
def log_in():
    if g.user.is_authenticated:
        flash(gettext('Вы уже вошли в систему под ником ') + current_user + '', 'error')
        return redirect(url_for('forum.topics'))
    form = SignInForm()
    forgot_form = ForgotPasswordForm()
    if request.method == 'POST':
        email = form.email.data,
        password = form.password.data
        registered_user = User.query.filter_by(email=email, password=password).first()
        if registered_user is None:
            flash(gettext('Неверное имя пользователя или пароль'), 'error')
            return redirect(url_for('user.log_in'))
        else:
            login_user(registered_user)
            flash(gettext('Вы успешно вошли в систему'))
            return redirect(url_for('forum.index'))

    return render_template('user/log_in.html',
                           form=form,
                           forgot_form=forgot_form,
                           title='Авторизация')


@user.route('logout', methods=['GET'])
@login_required
def log_out():
    logout_user()
    flash(gettext('Вы успешно вышли из системы'))
    return redirect(url_for('forum.index'))


@user.route('profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def show_profile_user(user_id):
    user_item = User.query.get_or_404(user_id)
    topics = user_item.topics.order_by('date_created desc').all()
    replies = user_item.replies.order_by('date_created desc').all()
    if user_item.id == g.user.id:
        return render_template('user/profile.html',
                               title='Профиль пользователя - ',
                               user=user_item,
                               topics=topics,
                               replies=replies)

    elif user_item.id != g.user.id:
        return render_template('user/profile.html',
                               title='Профиль пользователя - ',
                               user=user_item,
                               topics=topics,
                               replies=replies)


@user.route('members', methods=['GET'])
def members():
    all_members = User.query.all()
    return render_template('user/members.html', members=all_members)


@user.route('admin', methods=['GET', 'POST'])
def admin():
    if g.user.admin==False:
        flash(gettext('Нет доступа к админ панели'),'error')
        return redirect(url_for('forum.index'))

    return render_template('user/admin/index.html',
                           title="Администрирование")
