from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, Regexp, email

class LookupForm(Form):
    phone = StringField(u'Phone')
    submit = SubmitField(u'Submit')

class RegistrationForm(Form):
    name = StringField(u'Name')
    phone_1 = StringField(u'Phone #1')
    phone_2 = StringField(u'Phone #2')
    postcode = StringField(u'Postcode', validators=[Regexp('^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$', message='Postcode Invalid')])
    nationality = SelectField(u'Nationality', coerce=int)
    notes = TextAreaField(u'Notes')
    DoNotUse = BooleanField(u'Blacklist')
    submit = SubmitField('Submit')

class NationalityAddForm(Form):
    name = StringField(u'Name')
    submit = SubmitField('Submit')

class RoleAddForm(Form):
    name = StringField(u'Name')
    rate = StringField(u'Rate')
    department = SelectField(u'Department', choices=[('trade', 'Trades & Labour'), ('professional', 'Professional & Technical')])
    submit = SubmitField(u'Submit')
