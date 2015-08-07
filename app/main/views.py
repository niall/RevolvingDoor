from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import Staff, User, Nationality
from ..email import send_email
from . import main
from .forms import NameForm, RegistrationForm
from flask.ext.login import login_required

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

@main.route('/secret')
@login_required
def secret():
    return("Hahah")