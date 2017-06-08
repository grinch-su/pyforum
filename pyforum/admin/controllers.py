from flask import render_template, redirect, url_for, Response, flash, request
from flask_login import current_user, login_required
from flask_babel import _

from pyforum.admin import admin
from pyforum.user.models import User
from pyforum.forum.models import Category


@admin.route('/topics', methods=['GET', 'POST'])
@login_required
def admin_topics():
    if not current_user.admin:
        flash(_('Нет доступа к админ панели'), 'error')
        return redirect(url_for('forum.index'))
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('admin/tasks.html',
                               title=(_("Администрирование")),
                               categories=categories)


@admin.route('/users', methods=['GET', 'POST'])
@login_required
def admin_users():
    if not current_user.admin:
        flash(_('Нет доступа к админ панели'), 'error')
        return redirect(url_for('forum.index'))
    if request.method == 'GET':
        users = User.query.all()
        return render_template('admin/users.html',
                               title=(_("Администрирование")),
                               users=users)
