from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, email, ValidationError
from app.reg.utils import postcode_validate


class NewManagerForm(Form):
    name = StringField(u'Name')
    email = StringField(u'Email')
    phone = StringField(u'Phone')
    submit = SubmitField(u'Submit')



class NewSiteForm(Form):
    name = StringField(u'Site Name')
    address = StringField(u'Site Address')
    postcode = StringField(u'Site Postcode')
    start_time = StringField(u'Start Time')
    site_manager = SelectField(u'Site Manager', coerce=int)
    submit = SubmitField(u'Submit Field')

    def validate_postcode(form, field):
        if not postcode_validate(field.data):
            raise ValidationError('Enter valid postcode')

class NewCompanyForm(Form):
    name = StringField(u'Name')
    submit = SubmitField(u'Submit')

