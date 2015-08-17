from flask import render_template, redirect, url_for, flash
from .. import db
from ..models import User, Nationality, Role, Job
from . import reg
from .forms import RegistrationForm
from flask.ext.login import current_user
from .utils import map_lookup, journey

@reg.route('/')
def index():
    registered = User.query.order_by(User.registered.desc())
    return render_template('reg/index.html', registered=registered)


@reg.route('/new/', defaults={'phone': ''}, methods=['GET', 'POST'])
@reg.route('/new/<phone>')
def new(phone):
    form = RegistrationForm()
    form.nationality.choices = [(n.id, n.country) for n in Nationality.query.order_by('country')]
    form.role.choices = [(i.id, i.name) for i in Role.query.order_by('name')]
    if form.validate_on_submit():
        new_user = User(name=form.name.data,
                        phone_1=form.phone_1.data,
                        phone_2=form.phone_2.data,
                        email=form.email.data,
                        postcode=form.postcode.data.replace(" ", "").upper(),
                        notes=form.notes.data,
                        DoNotUse=form.DoNotUse.data,
                        role_id = form.role.data,
                        nationality_id=form.nationality.data,
                        added_id=current_user.id)
        db.session.add(new_user)
        flash('Added User: ' + new_user.name)
        return redirect(url_for('reg.profile', type='name', value=new_user.name))
    if form.phone_1.data is None:
        form.phone_1.data = phone
    return render_template('reg/new-register.html', form=form)
"""
@user.route('/<user_id>', defaults={'username': None})
@user.route('/<user_id>/<username>')
def show(user_id, username):
    pass
"""
@reg.route('/<type>/<value>')
def profile(type, value):
    kwargs = {type: value}
    user = User.query.filter_by(**kwargs).first_or_404()
    map_url = map_lookup(user.postcode)
    jobs = Job.query.filter_by(role_id=user.role_id).all()

    distance = []
    duration = []
    for i in range(len(jobs)):
        result = journey(jobs[i].site.postcode, user.postcode)
        distance.append(result[0])
        duration.append(result[1])
    n=len(jobs)
    return render_template('reg/reg-profile.html', user=user, map_url=map_url, n=n, jobs=jobs, distance=distance, duration=duration)

@reg.route('/<type>/<value>/edit', methods=['GET', 'POST'])
def edit_profile(type, value):
    kwargs = {type: value}
    user = User.query.filter_by(**kwargs).first_or_404()
    form = RegistrationForm()
    form.nationality.choices = [(n.id, n.country) for n in Nationality.query.order_by('country')]
    form.role.choices = [(i.id, i.name) for i in Role.query.order_by('name')]
    if form.validate_on_submit():
        user.name = form.name.data
        user.phone_1 = form.phone_1.data
        user.phone_2 = form.phone_2.data
        user.role_id = form.role.data
        user.email = form.email.data
        user.postcode = form.postcode.data
        user.nationality_id = form.nationality.data
        flash(user.name + " Updated")
        return redirect(url_for('reg.profile', type='id', value=user.id))
    #Fill Form
    form.name.data = user.name
    form.phone_1.data = user.phone_1
    form.phone_2.data = user.phone_2
    form.role.data = user.role_id
    form.email.data = user.email
    form.postcode.data = user.postcode
    form.nationality.data = user.nationality_id
    return render_template('reg/edit-profile.html', form=form, user=user)