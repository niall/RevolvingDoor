from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, email, ValidationError, Optional
from app.reg.utils import postcode_validate
from wtforms.fields.html5 import DateField

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

class NewJobForm(Form):
    site = SelectField(u'Site', coerce=int)
    role = SelectField(u'Role', coerce=int)
    start_date = DateField(u'Start Date')
    end_date = DateField(u'End Date (Optional)', validators=[Optional()])
    number = SelectField(u'Number of workers', choices=[('1', '1'), ('2', '2'), ('3', '3'),
                        ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    submit = SubmitField(u'Submit')
