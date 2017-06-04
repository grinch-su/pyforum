import json
from datetime import datetime

from itsdangerous import URLSafeTimedSerializer
from flask import render_template, redirect, url_for, Response, jsonify, flash, request, g, current_app, abort, make_response
from flask_login import logout_user, login_required, login_user, current_user, AnonymousUserMixin
from flask_babel import _

from config import Config
from pyforum import db, login_manager, app, babel
from pyforum.utils.email import send_confirmation_email, send_reset_password
from pyforum.user import user
from pyforum.user.models import User, Anonymous
from pyforum.forum.models import Topic, Reply, Category
from pyforum.user.forms import SignUpForm, SignInForm, ResetEmailForm, ResetPasswordForm

login_manager.anonymous_user = Anonymous

# babel
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(Config.SUPPORTED_LANGUAGES.keys())


@babel.timezoneselector
def get_timezone():
    user = g.get('user', None)
    if user is not None:
        return user.timezone


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash(_('Пожалуйста авторизируйтесь!'))
    return redirect(url_for('user.log_in'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_visit = datetime.utcnow()
        db.session.commit()
    if g.user.banned:
        return render_template('user/auth/banned.html')


@user.route('signup', methods=['GET', 'POST'])
def sign_up():
    if g.user.is_authenticated:
        flash(_('Вы уже вошли в систему под ником {username}').format(username=g.user.username), 'error')
        return redirect(url_for('forum.index'))
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)

        new_user.ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        db.session.add(new_user)
        db.session.commit()

        send_confirmation_email(new_user.email)

        flash(_('Пожалуйста, проверьте свой адрес электронной почты, '
                'чтобы подтвердить свой адрес электронной почты'), 'info')

        return redirect(url_for('forum.index'))

    return render_template('user/auth/sign_up.html', form=form)


@user.route('confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = confirm_serializer.loads(token,
                                         salt='email-confirmation-salt',
                                         max_age=3600)
    except:
        flash(_('Ссылка подтверждения недействительна или время истекло.'), 'error')
        return redirect(url_for('user.login'))

    user = User.query.filter_by(email=email).first()

    if user.activated:
        flash('Аккаунт уже подтвержден.', 'success')
    else:
        user.activated = True
        db.session.add(user)
        db.session.commit()
        flash(_('Спасибо, что подтвердили свой адрес электронной почты!'), 'success')
    return redirect(url_for('forum.index'))


@user.route('login', methods=['GET', 'POST'])
def log_in():
    if current_user.is_authenticated:
        flash(_('Вы уже вошли в систему под ником {user}'.format(user=current_user.username)), 'error')
        return redirect(url_for('forum.index'))
    form = SignInForm()
    if form.validate_on_submit():
        registered_user = User.query.filter_by(email=form.email.data,
                                               password=form.password.data).first()
        if registered_user is None:
            flash(_('Неверный эл. адрес или пароль'), 'error')
            return redirect(url_for('user.log_in'))
        else:
            login_user(registered_user)
            flash(_('Вы успешно вошли в систему'), 'success')
            return redirect(url_for('forum.index'))

    form_reset = ResetEmailForm()
    if form_reset.validate_on_submit():
        reset_user = User.query.filter_by(email=form_reset.email.data).first_or_404()

        send_reset_password(reset_user.email)
        flash(_('Проверьте почту'), 'info')
        return redirect(url_for('forum.index'))

    return render_template('user/auth/log_in.html',
                           form=form,
                           form_reset=form_reset,
                           title=(_('Авторизация')))


@user.route('reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = confirm_serializer.loads(token,
                                         salt='email-confirmation-salt',
                                         max_age=3600)
    except:
        flash(_('Ссылка восстановления более не действительна: время её действия истекло или она уже была использована ранее.'), 'error')
        return redirect(url_for('user.login'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        reset_user = User.query.filter_by(email=email).first_or_404()

        reset_user.password = form.password.data

        db.session.add(reset_user)
        db.session.commit()

        return redirect(url_for('user.log_in'))

    return render_template('user/auth/reset_with_token.html',
                           title='Восстановление пароля',
                           form=form,
                           token=token)


@user.route('logout', methods=['GET'])
@login_required
def log_out():
    logout_user()
    flash(_('Вы успешно вышли из системы'), 'success')
    return redirect(url_for('user.log_in'))


@user.route('profile/<string:username>', methods=['GET', 'POST'])
@login_required
def show_profile_user(username):
    user_item = User.query.filter_by(username=username).first_or_404()
    topics = user_item.topics.order_by('date_created desc').all()
    replies = user_item.replies.order_by('date_created desc').all()
    if user_item.id == g.user.id:
        return render_template('user/profile.html',
                               title=(_('Профиль пользователя - ')),
                               user=user_item,
                               topics=topics,
                               replies=replies)

    elif user_item.id != g.user.id:
        return render_template('user/profile.html',
                               title=(_('Профиль пользователя - ')),
                               user=user_item,
                               topics=topics,
                               replies=replies)


@user.route('profile/edit/<string:username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    if username != current_user.username:
        flash(_('Вы не можете редактировать чужие профили'), 'error')
        return redirect(url_for('user.edit_profile', username=current_user.username))
    edit_user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        edit_user.username = request.form.get('username')
        edit_user.password = request.form.get('password')
        edit_user.web_site = request.form.get('web-site')
        edit_user.birth_day = request.form.get('birth-day')
        edit_user.signature = request.form.get('signature')
        db.session.commit()
        return redirect(url_for('user.show_profile_user', username=username))
    else:
        return render_template('user/edit_profile.html',
                               title=(_('Редактирование профиля')),
                               user=edit_user)


@user.route('members', methods=['GET', 'POST'])
def members():
    new_five_members = User.query.order_by(User.date_joined.desc()).limit(5).all()
    return render_template('user/members.html',
                           members=new_five_members)


@user.route('admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.admin:
        flash(_('Нет доступа к админ панели'), 'error')
        return redirect(url_for('forum.index'))
    if request.method == 'GET':
        categories = Category.query.all()
        users = User.query.all()
        return render_template('user/admin/index.html',
                               title=(_("Администрирование")),
                               categories=categories,
                               users=users)
