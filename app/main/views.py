from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from . import main
from ..models import User, Movies
from .forms import EditProfileForm, AddURLCinemaForm
from .. import db
from ..utils import get_response


@main.route('/', methods=['GET', 'POST'])
def index():
    form = AddURLCinemaForm()
    if form.validate_on_submit():
        if current_user.movie_already_added(form.url.data):
            flash('The movie has already been added to your collection.')
            return redirect(url_for('main.index'))

        title, year, type_, description, runtime, poster = \
            get_response(form.url.data)
        movie = Movies(title=title,
                       year=year,
                       type=type_,
                       description=description,
                       runtime=runtime,
                       poster=poster,
                       url=form.url.data)
        current_user.add_movie(movie)
        db.session.commit()
        flash('Movie added successfully')
        return redirect(url_for('main.index'))

    return render_template('index.html', form=form)


@main.route('/profile/<username>')
def profile_username(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.profile_username', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
