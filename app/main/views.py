from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import Staff, User
from ..email import send_email
from . import main
from .forms import NameForm, RegistrationForm

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(username=form.name.data).first()
        if staff is None:
            staff = Staff(username=form.name.data)
            db.session.add(staff)
            session['known'] = False
            send_email(current_app.config['RD_ADMIN'], 'New Registration', 'mail/test', staff=staff)
        else:
            session['known'] = True
            flash('Name not added')
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'))

@main.route('/user/<name>')
def user(name):
    form = NameForm()
    return render_template('user.html', name=name)

@main.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, postcode=form.postcode.data)
        db.session.add(user)
        flash('Registered')
    return render_template('register.html', form=form)