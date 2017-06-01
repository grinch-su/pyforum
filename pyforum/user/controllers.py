from datetime import datetime

from itsdangerous import URLSafeTimedSerializer
from flask import render_template, redirect, url_for, Response, jsonify, flash, request, g, current_app, abort
from flask_login import logout_user, login_required, login_user, current_user, AnonymousUserMixin
from flask_babel import gettext, _

from config import Config
from pyforum import db, login_manager, app, babel
from pyforum.utils.email import send_email
from pyforum.user import user
from pyforum.user.models import User, Anonymous
from pyforum.forum.models import Topic, Reply, Category
from pyforum.user.forms import SignUpForm, SignInForm, ForgotPasswordForm


login_manager.login_view = 'user.log_in'
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


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

    confirm_url = url_for('user.confirm_email',
                          token=confirm_serializer.dumps(user_email,
                                                         salt='email-confirmation-salt'),
                          _external=True)

    html = render_template('user/email_confirmation.html',
                           confirm_url=confirm_url)

    send_email('Подтвердите Ваш электронный адрес',
               [user_email],
               text_body='Подтвердите адрес эл.почты',
               html_body=html)


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
                        password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        send_confirmation_email(new_user.email)
        flash(_('Спасибо за регистрацию! Пожалуйста, проверьте свой адрес электронной почты, чтобы подтвердить свой адрес электронной почты'), 'success')

        return redirect(url_for('forum.index'))

    return render_template('user/sign_up.html', form=form)


@user.route('confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = confirm_serializer.loads(token,
                                         salt='email-confirmation-salt',
                                         max_age=3600)
    except:
        flash(gettext('Ссылка подтверждения недействительна или истекло время.'), 'error')
        return redirect(url_for('user.login'))

    user = User.query.filter_by(email=email).first()

    if user.activated:
        flash('Аккаунт уже подтвержден.', 'info')
    else:
        user.activated = True
        db.session.add(user)
        db.session.commit()
        flash(gettext('Спасибо, что подтвердили свой адрес электронной почты!'))
    return redirect(url_for('forum.index'))

@user.route('login', methods=['GET', 'POST'])
def log_in():
    if current_user.is_authenticated:
        flash(gettext('Вы уже вошли в систему под ником ') + current_user + '', 'error')
        return redirect(url_for('forum.topics'))
    form = SignInForm()
    forgot_form = ForgotPasswordForm()
    if request.method == 'POST':
        email = form.email.data,
        password = form.password.data
        registered_user = User.query.filter_by(email=email,
                                               password=password).first()
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
                           title=(gettext('Авторизация')))


@user.route('logout', methods=['GET'])
@login_required
def log_out():
    logout_user()
    flash(_('Вы успешно вышли из системы'),'success')
    return redirect(url_for('forum.index'))


@user.route('profile/<string:username>', methods=['GET', 'POST'])
@login_required
def show_profile_user(username):
    user_item = User.query.filter_by(username=username).first_or_404()
    topics = user_item.topics.order_by('date_created desc').all()
    replies = user_item.replies.order_by('date_created desc').all()
    if user_item.id == g.user.id:
        return render_template('user/profile.html',
                               title=(gettext('Профиль пользователя - ')),
                               user=user_item,
                               topics=topics,
                               replies=replies)

    elif user_item.id != g.user.id:
        return render_template('user/profile.html',
                               title=(gettext('Профиль пользователя - ')),
                               user=user_item,
                               topics=topics,
                               replies=replies)


@user.route('profile/edit/<string:username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    return render_template('user/edit_profile.html',
                           title=(gettext('Редактирование профиля')))


@user.route('members', methods=['GET', 'POST'])
def members():
    members = User.query.order_by(User.date_joined.desc()).limit(5).all()
    return render_template('user/members.html',
                           members=members)


@user.route('admin', methods=['GET', 'POST'])
def admin():
    if current_user.admin == False:
        flash(gettext('Нет доступа к админ панели'), 'error')
        return redirect(url_for('forum.index'))
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('user/admin/index.html',
                               title=(gettext("Администрирование")),
                               categories=categories)
