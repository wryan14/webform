from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
'''
These fields are dummy fields, and will be used as placeholders until I gather more information
on which fields are needed.  Flask forms allows for more complicated data structures and validation,
so work will resume on this once the project structure is in place.
'''

class NewPublication(FlaskForm):
    '''Creates form field for new publication'''

    # adding small set of dummy data for setup purposes
    name = StringField("Name: ")
    submit = SubmitField('Submit')


class UpdatePublication(FlaskForm):
    '''Creates form fields for update publication'''

    name = StringField("Name: ")
    submit = SubmitField('Submit')


class UpdatePublicationStatus(FlaskForm):
    '''Creates form fields for publication status'''

    name = StringField("Name: ")
    submit = SubmitField('Submit')
