from flask import render_template, redirect, url_for, Response
from flask_login import current_user

from pyforum.general import general


@general.app_errorhandler(404)
def page_not_found(e):
    return render_template('general/404.html'), 404


@general.app_errorhandler(500)
def server_error(e):
    return render_template('general/500.html'), 500
