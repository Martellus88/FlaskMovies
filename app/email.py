from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_threading_email(app, msg):
    with app.app_cotext():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(
        subject=f"{current_app.config['FLASK_MOVIE_SUBJECT']} {subject}",
        sender=current_app.config['FLASK_MOVIE_SENDER'],
        recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.body = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_threading_email, args=[current_app, msg])
    thread.start()
    return thread