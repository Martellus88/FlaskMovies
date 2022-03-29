import datetime
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    def __repr__(self):
        return f'<User> {self.id=}:{self.username=}:{self.email=}'

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
        return jwt.encode({'confirm': self.id, 'exp': expiration_time},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256')

    def confirm_register_token(self, token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_mail_change_token(self, new_email, expiration=3600):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
        return jwt.encode({'change_email': self.id, 'new_email': new_email, 'exp': expiration_time},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256')

    def change_email(self, token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return False
        if data['change_email'] != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def generate_reset_password_token(self, expiration=3600):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
        return jwt.encode({'reset_password': self.id, 'exp': expiration_time},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256')

    def reset_password(token, new_password):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return False
        user = User.query.get(data.get('reset_password'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
