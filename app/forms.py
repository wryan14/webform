# forms.py
# File contains all of the Flask form-fields required to add, edit, and update publications

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, Form, FormField
from wtforms.validators import DataRequired

class AuthorForm(Form):
    """Form that inherits from wtforms.Form class. Contains fields for author 
        first_name and last_name
    """
    first_name = StringField('First Name')
    last_name = StringField('Last Name')


class NewPublication(FlaskForm):
    """Contains the form-fields required to add a new publication. The author
        FieldList allows for up to 30 authors.
    """

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
    """Contains the form-fields required to update a publication. The author
    FieldList allows for up to 30 authors.
    """

    title = StringField("Title ")
    doi = StringField("DOI ")
    publication = StringField("Published in")

    authors = FieldList(
        FormField(AuthorForm),
        min_entries=1,
        max_entries=30
    )

    submit = SubmitField('Submit')


class UpdatePublicationStatus(FlaskForm):
    """[IN PROGRESS] This will contain the form-fields required to udpate a 
    forthcoming publication. 
    """

    title = StringField("Title ")
    submit = SubmitField('Submit')
