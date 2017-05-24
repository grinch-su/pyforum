from flask import render_template, redirect, url_for, Response, jsonify, flash, request, g, current_app, abort
from flask_login import logout_user, login_required, login_user, current_user

from pyforum import db, login_manager
from pyforum.user import user
from pyforum.user.models import User,Group
from pyforum.user.forms import SignUpForm, SignInForm, ForgotPasswordForm


@user.route('signup', methods=['GET', 'POST'])
def sign_up():
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
    form = SignInForm()
    forgot_form = ForgotPasswordForm()
    if request.method == 'POST':
        email=form.email.data,
        password=form.password.data
        registered_user = User.query.filter_by(email=email, password=password).first()
        if registered_user is None:
            flash('Неверное имя пользователя или пароль', 'error')
            return redirect(url_for('user.log_in'))
        else:
            login_user(registered_user)
            flash('Вы успешно вошли в систему')
            return redirect(url_for('forum.topics'))
    return render_template('user/log_in.html',
                           form = form,
                           forgot_form = forgot_form,
                           title = 'Авторизация')


@user.route('logout', methods=['GET'])
@login_required
def log_out():
    logout_user()
    flash('Вы успешно вышли из системы')
    return redirect(url_for('forum.topics'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@user.before_request
def before_request():
    g.user = current_user


@user.route('profile/<int:user_id>', methods=['GET', 'POST'])
def show_profile_user(user_id):
    user_item = User.query.get(user_id)
    if user_item.id == g.user.id:
        return render_template('user/profile.html',
                           title='Профиль пользователя - ',
                           user  = user_item)
    elif user_item.id != g.user.id:
        flash('Не равно текущему ид')
        return render_template('user/profile.html',
                           title='Профиль пользователя - ',
                           user  = user_item)
    elif user_item.id is None:
        return abort(404, error = 'Пользоателя с таким ид нет')


@user.route('members', methods=['GET'])
def members():
    members = User.query.all()
    return render_template('user/members.html', members=members)
