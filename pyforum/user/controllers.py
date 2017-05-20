from flask import render_template, redirect, url_for
from flask_login import logout_user, login_required

from pyforum.user import user
from pyforum.user.models import User,Group
from pyforum.user.forms import SignUpForm, SignInForm, ForgotPasswordForm

@user.route('members', methods=['GET'])
def members():
    return render_template('user/members.html')


@user.route('login', methods=['GET', 'POST'])
def log_in():
    form = SignInForm()
    forgot_form = ForgotPasswordForm()
    return render_template('user/log_in.html',
                           form = form,
                           forgot_form = forgot_form,
                           title = 'Авторизация')


@user.route('logout', methods=['GET'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for('forum.topics'))


@user.route('signup', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        print(user)
        return redirect(url_for('forum.topics'))

    return render_template('user/sign_up.html', form=form)
