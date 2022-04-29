from app import movintoryApp
from flask import render_template, request


@movintoryApp.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html', error=e)


@movintoryApp.errorhandler(413)
def entity_too_large(e):
    return render_template('errors/413.html', error=e)


@movintoryApp.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', error=e)