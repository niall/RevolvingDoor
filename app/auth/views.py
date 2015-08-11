from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import Staff
from .forms import LoginForm, ChangePasswordForm, EditStaffForm, NewStaffForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(email=form.email.data).first()
        if staff is not None and staff.verify_password(form.password.data):
            login_user(staff, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid Username or Password')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            flash('Password has been changed')
            current_user.password = form.password.data
            db.session.add(current_user)
        else:
            flash('Old Password is not valid, Password not changed!')
        return redirect(url_for('auth.change_password'))
    return render_template('auth/change-password.html', form=form)

@auth.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditStaffForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.name = form.name.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.staff', name=current_user.username))
    form.email.data = current_user.email
    form.name.data = current_user.name
    return render_template('auth/edit-company-reg-profile.html', form=form)

@auth.route('/new', methods=['GET', 'POST'])
def new_staff():
    form = NewStaffForm()
    if form.validate_on_submit():
        staff = Staff(username=form.username.data, email=form.email.data, name=form.name.data, password=form.password.data)
        db.session.add(staff)
        return redirect(url_for('.staff', name=staff.username))
    return render_template('auth/edit-profile.html', form=form)

@auth.route('/')
def list_staff():
    staff = Staff.query.all()
    return render_template('auth/list-staff.html', staff=staff)

@auth.route('/<name>')
def staff(name):
    staff = Staff.query.filter_by(username=name).first_or_404()
    return render_template('auth/staff.html', staff=staff)