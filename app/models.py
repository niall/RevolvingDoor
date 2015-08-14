from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager
from datetime import datetime

class Staff(db.Model, UserMixin):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    added = db.relationship('User', backref='added_by')

    def __repr__(self):
        return '<Staff %r>' % self.username

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    registered = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    name = db.Column(db.String(64))
    phone_1 = db.Column(db.String(64))
    phone_2 = db.Column(db.String(64))
    email = db.Column(db.String(64))
    notes = db.Column(db.Text)
    area = db.Column(db.String(64))
    postcode = db.Column(db.String(64))
    DoNotUse = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    nationality_id = db.Column(db.Integer, db.ForeignKey('nationality.id'))
    added_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    job_id = db.relationship('Job', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

class Nationality(db.Model):
    __tablename__ = 'nationality'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(64))
    users = db.relationship('User', backref='nationality')

    def __init__(self, country):
        self.country = country

    def __repr__(self):
        return '<Nationality %r>' % self.country

class Site(db.Model):
    __tablename__ = 'sites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    address = db.Column(db.String(64))
    postcode = db.Column(db.String(16))
    start_time = db.Column(db.String(8))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    site_manager = db.relationship('SiteManager', backref='site', lazy='dynamic')
    jobs = db.relationship('Job', backref='site', lazy='dynamic')

    def __repr__(self):
        return '<Site: %r>' % self.name

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    sites = db.relationship('Site', backref='company', lazy='dynamic')
    managers = db.relationship('SiteManager', backref='company', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Company: %r>' % self.name

    class Meta:
        ordering = (('id', 'desc'),)

class SiteManager(db.Model):
    __tablename__ = 'site_managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))

    def __repr__(self):
        return '<Site Manager: %r>' % self.name

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    department = db.Column(db.String(16))
    rate = db.Column(db.String(16))
    users = db.relationship('User', backref='role', lazy='dynamic')
    job_id = db.relationship('Job', backref='role', lazy='dynamic')

    def __init__(self, name, department, rate):
        self.name = name
        self.department = department
        self.rate = rate

    def __repr__(self):
        return '<Role: %r>' % self.name


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def __repr__(self):
        return '<Job: %r for %r (%r) ID#%r>' %(self.role.name, self.site.name, self.site.company.name, self.id)


@login_manager.user_loader
def load_user(staff_id):
    return Staff.query.get(int(staff_id))



