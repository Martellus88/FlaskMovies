from flask import render_template
from . import main
from ..models import User


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile/<username>')
def profile_username(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)
