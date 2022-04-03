from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors.html', title='Page Not Found'), error.code


@main.app_errorhandler(403)
def forbidden(error):
    return render_template('errors.html', title='Forbidden'), error.code


@main.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors.html', title='Internal Server Error'), error.code
