from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class AddURLCinemaForm(FlaskForm):
    url = StringField('Link to imdb or kinopoisk', validators=[
        DataRequired(),
        Regexp("^(https?:\/\/)?(www.imdb.com|www.kinopoisk.ru)[^\s@]*")],
                      render_kw={
                          "placeholder": "example: https://www.imdb.com/title/tt0133093/ or https://www.kinopoisk.ru/film/301/"})
    submit = SubmitField('Add cinema')
