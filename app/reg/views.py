from flask import render_template, redirect, url_for, flash
from .. import db
from ..models import User, Nationality
from . import reg
from .forms import RegistrationForm
from flask.ext.login import current_user
from .utils import map_lookup

@reg.route('/')
def index():
    registered = User.query.order_by(User.registered.desc())
    return render_template('reg/index.html', registered=registered)

@reg.route('/new', methods=['GET', 'POST'])
def new():
    form = RegistrationForm()
    form.nationality.choices = [(n.id, n.country) for n in Nationality.query.order_by('country')]
    if form.validate_on_submit():
        new_user = User(name=form.name.data,
                        phone_1=form.phone_1.data,
                        phone_2=form.phone_2.data,
                        email=form.email.data,
                        postcode=form.postcode.data.replace(" ", "").upper(),
                        notes=form.notes.data,
                        DoNotUse=form.DoNotUse.data,
                        nationality_id=form.nationality.data,
                        added_id=current_user.id)
        db.session.add(new_user)
        flash('Added User: ' + new_user.name)
        return redirect(url_for('reg.name', type='name', value=new_user.name))
    return render_template('reg/new-register.html', form=form)

@reg.route('/<type>/<value>')
def name(type, value):
    kwargs = {type: value}
    user = User.query.filter_by(**kwargs).first_or_404()
    map_url = map_lookup(user.postcode)
    return render_template('reg/reg-profile.html', user=user, map_url=map_url)
