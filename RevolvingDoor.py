import os
from flask import Flask, render_template, redirect, session, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail, Message
from flask.ext.script import Shell

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# Email Configs:
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] ='fomac.auto@gmail.com'
app.config['MAIL_PASSWORD'] ='FoMac9001!'
app.config['RD_MAIL_SUBJECT_PREFIX'] = '[Fomac - Automatic:]'
app.config['RD_MAIL_SENDER'] = 'Fomac - No Reply <fomac.auto@gmail.com>'

# Initialise
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
manager.add_command('db', MigrateCommand)

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<Staff %r>' % self.username

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['RD_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['RD_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

def make_shell_context():
    return dict(app=app, db=db, Staff=Staff)
manager.add_command("shell", Shell(make_context=make_shell_context))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(username=form.name.data).first()
        if staff is None:
            staff = Staff(username=form.name.data)
            db.session.add(staff)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    form = NameForm()
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()

