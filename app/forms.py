from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, Form, FormField
from wtforms.validators import DataRequired
'''
These fields are dummy fields, and will be used as placeholders until I gather more information
on which fields are needed.  Flask forms allows for more complicated data structures and validation,
so work will resume on this once the project structure is in place.
'''

class AuthorForm(Form):
    """Subform.

    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    first_name = StringField('First Name')
    last_name = StringField('Last Name')


class NewPublication(FlaskForm):
    '''Creates form field for new publication'''

    # adding small set of dummy data for setup purposes
    doi = StringField('DOI ')
    title = StringField("Title ", validators=[DataRequired()])
    publisher = StringField("Publisher ")
    publication = StringField("Published in ")
    year = StringField('Publication Year')

    authors = FieldList(
        FormField(AuthorForm),
        min_entries=1,
        max_entries=30
    )
 
    submit = SubmitField('Submit')
    


class UpdatePublication(FlaskForm):
    '''Creates form fields for update publication'''

    title = StringField("Title ")

    authors = FieldList(
        FormField(AuthorForm),
        min_entries=1,
        max_entries=30
    )

    submit = SubmitField('Submit')


class UpdatePublicationStatus(FlaskForm):
    '''Creates form fields for publication status'''

    title = StringField("Title ")
    submit = SubmitField('Submit')
