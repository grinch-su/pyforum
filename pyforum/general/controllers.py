"""
general module
"""
from flask import render_template, redirect, url_for, Response

from pyforum.general import general


@general.app_errorhandler(404)
def page_not_found(e):
    # обработка 404 ошибки
    return render_template('general/404.html'), 404


@general.app_errorhandler(500)
def server_error(e):
    # обработка 500 ошибки
    return render_template('general/500.html'), 500
