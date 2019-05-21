from flask import render_template
from lib.scripts import user_logged_in


def not_found(error):
    return render_template('not-found.html', pageTitle='Not Found', navBar=True, logged_in=user_logged_in()), 404


def server_error(error):
    print(error)
    return render_template('server-error.html', pageTitle='Not Found', navBar=True, logged_in=user_logged_in()), 500
