from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from . import main
from ..models import User, Movies
from .forms import EditProfileForm, AddURLCinemaForm
from .. import db
from ..utils import get_response


def _get_collection_video(username, type_video):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.movies.filter_by(type=type_video).paginate(
        page, per_page=current_app.config['MOVIES_PER_PAGE'], error_out=False)
    movies = pagination.items
    return render_template('collection.html', movies=movies, user=user, pagination=pagination, h1=type_video)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = AddURLCinemaForm()
    if form.validate_on_submit():
        if current_user.movie_already_added(form.url.data.strip()):
            flash('The movie has already been added to your collection.')
            return redirect(url_for('main.index'))

        movie = Movies.query.filter_by(url=form.url.data.strip()).first()
        if movie is not None:
            current_user.add_movie(movie)
        else:
            title, year, type_, description, runtime, poster = \
                get_response(form.url.data.strip())
            movie = Movies(title=title,
                           year=year,
                           type=type_,
                           description=description,
                           runtime=runtime,
                           poster=poster,
                           url=form.url.data.strip())
            current_user.add_movie(movie)

        db.session.commit()
        flash('Movie added successfully')
        return redirect(url_for('main.index'))

    return render_template('index.html', form=form)


@main.route('/profile/<username>')
@login_required
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


@main.route('/movie_collection/<username>')
@login_required
def movie_collection(username):
    return _get_collection_video(username, 'movie')


@main.route('/series_collection/<username>')
@login_required
def series_collection(username):
    return _get_collection_video(username, 'series')


@main.route('/movie/<int:id>')
@login_required
def movie(id):
    movie = Movies.query.get_or_404(id)
    return render_template('movie.html', movie=movie)


@main.route('/delete_movie_collection/<int:id>')
@login_required
def delete_movie(id):
    movie = Movies.query.get_or_404(id)
    current_user.movies.remove(movie)
    db.session.commit()
    return redirect(url_for('.movie_collection', username=current_user.username))
