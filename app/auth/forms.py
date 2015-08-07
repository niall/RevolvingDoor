from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(Form):
    email = StringField('E-Mail', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password')
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Field must match \'New Password\'')])
    submit = SubmitField('Change Password')

class EditStaffForm(Form):
    email = StringField(u'Email')
    name = StringField(u'Name')
    submit = SubmitField('Submit')

class NewStaffForm(Form):
    username = StringField(u'Username')
    email = StringField(u'Email')
    name = StringField(u'Name')
    password = PasswordField(u'Password')
    submit = SubmitField(u'Submit')

