from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<Staff %r>' % self.username

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    registered = db.Column(db.DateTime)
    name = db.Column(db.String(64))
    phone_1 = db.Column(db.String(64))
    phone_2 = db.Column(db.String(64))
    notes = db.Column(db.Text)
    postcode = db.Column(db.String(64))
    DoNotUse = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r - %r>' % self.name,

