from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired
'''
These fields are dummy fields, and will be used as placeholders until I gather more information
on which fields are needed.  Flask forms allows for more complicated data structures and validation,
so work will resume on this once the project structure is in place.
'''

class NewPublication(FlaskForm):
    '''Creates form field for new publication'''

    # adding small set of dummy data for setup purposes
    doi = StringField('DOI ')
    title = StringField("Title ", validators=[DataRequired()])
    publisher = StringField("Publisher ")
    publication = StringField("Published in ")
    year = StringField('Publication Year')
 
    submit = SubmitField('Submit')
    


class UpdatePublication(FlaskForm):
    '''Creates form fields for update publication'''

    title = StringField("Title ")
    submit = SubmitField('Submit')


class UpdatePublicationStatus(FlaskForm):
    '''Creates form fields for publication status'''

    title = StringField("Title ")
    submit = SubmitField('Submit')
