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
    nationality_id = db.Column(db.Integer, db.ForeignKey('nationality.id'))
    added_id = db.Column(db.Integer, db.ForeignKey('staff.id'))

    def __repr__(self):
        return '<User %r>' % self.name

class Nationality(db.Model):
    __tablename__ = 'nationality'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(64))
    users = db.relationship('User', backref='nationality')

    def __repr__(self):
        return '<Nationality %r>' % self.country


@login_manager.user_loader
def load_user(staff_id):
    return Staff.query.get(int(staff_id))