import os
from threading import Thread

from flask import Flask, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'secret string'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('bsholy', os.getenv('MAIL_USERNAME'))
)

mail = Mail(app)


def send_smtp_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)


def _send_async_mail(app_, message):
    with app_.app_context():
        mail.send(message)


def send_async_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


@app.route('/')
def index():
    return "Hello, world!"


@app.route('/send_test_mail')
def send_test_mail():
    subject = 'Hello, world!'
    to = '2784191947@qq.com'
    body = 'Across the Great Wall we can reach every corner in the world.'
    send_smtp_mail(subject, to, body)
    return redirect('index')


@app.route('/send_async_test_mail')
def send_async_test_mail():
    subject = 'Hello, world!'
    to = '2784191947@qq.com'
    body = 'This is a async mail.'
    send_async_mail(subject, to, body)
    return redirect(url_for('index'))

