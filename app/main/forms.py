from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Regexp, email

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegistrationForm(Form):
    name = StringField('Name')
    phone_1 = StringField('Phone #1')
    phone_2 = StringField('Phone #2')
    postcode = StringField('Postcode', validators=[Regexp('^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$', message='Postcode Invalid')])
    notes = TextAreaField('Notes')
    DoNotUse = BooleanField('Blacklist')
    submit = SubmitField('Submit')