from datetime import date, timedelta
from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import Staff, User, Nationality, Company, Role, Job
from ..email import send_email
from . import main
from .forms import LookupForm, NationalityAddForm, RoleAddForm
from flask.ext.login import login_required, current_user

@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated():
        form = LookupForm()
        tomorrow = date.today() + timedelta(days=1)
        jobs = Job.query.filter_by(start_date=tomorrow).all()

        sites = []
        for job in jobs:
            sites.append(job.site)
        sites = list(set(sites))

        if form.validate_on_submit():
            user = User.query.filter_by(phone_1=form.phone.data).first()
            if user is None:
                flash('No user exists with that number')
                return redirect(url_for('reg.new', phone=form.phone.data))
            else:
                flash('User with that number exists')
                return redirect(url_for('reg.profile', type='phone_1', value=form.phone.data))
        return render_template('index.html', form=form, jobs=jobs, sites=sites, tomorrow=tomorrow)
    else:
        return redirect(url_for('auth.login'))

@main.route('/nationality', methods=['GET', 'POST'])
def add_nationality():
    form = NationalityAddForm()
    if form.validate_on_submit():
        db.session.add(Nationality(form.name.data))
        flash('Nationality Added: ' + form.name.data)
        return redirect(url_for('main.add_nationality'))
    return render_template('nationality.html', form=form)

@main.route('/roles', methods=['GET', 'POST'])
def add_role():
    form = RoleAddForm()
    role = Role.query.all()
    if form.validate_on_submit():
        exist = Role.query.filter_by(name=form.name.data).first()
        if exist:
            flash('Role ' + form.name.data + ' already exists')
            return redirect(url_for('main.add_role'))
        else:
            flash('Role ' + form.name.data + ' added')
            db.session.add(Role(form.name.data, form.department.data, form.rate.data))
            return redirect(url_for('main.add_role'))
    return render_template('role.html', form=form, role=role)

@main.route('/jobs')
def jobs():
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)

@main.route('/secret')
@login_required
def secret():
    return(render_template('test.html'))
