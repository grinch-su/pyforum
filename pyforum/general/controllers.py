from flask import render_template, redirect, url_for, Response
from pyforum.general import general
from pyforum.general.forms import SearchForm


@general.route('search', methods=['GET','POST'])
def search():
    form_search = SearchForm()
    if form_search.validate_on_submit():
        pass
    return render_template('general/search.html', form_search=form_search)


@general.app_errorhandler(401)
def page_not_found(e):
    return Response('Ошибка авторизации'), 401


@general.app_errorhandler(404)
def page_not_found(e):
    return render_template('general/404.html'), 404


@general.app_errorhandler(500)
def server_error(e):
    return render_template('general/500.html'), 500
