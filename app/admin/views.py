from flask import render_template, flash, redirect, url_for
from .. import db
from ..models import User
from .forms import EditProfileAdmin
from . import admin
from ..decorators import admin_required


@admin.route('/')
@admin_required
def admin_page():
    users = User.query.order_by().all()
    return render_template('admin_panel/admin.html', users=users)


@admin.route('/edit_user_profile/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_user_profile(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdmin(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.admin_page'))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form)


@admin.route('/delete_user_profile/<int:id>')
@admin_required
def delete_user_profile(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.')
    return redirect(url_for('.admin_page'))
