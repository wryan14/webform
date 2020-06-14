from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class NewPublication(FlaskForm):
    '''Creates form field for new publication'''

    # adding small set of dummy data for setup purposes
    name = StringField("Name: ")
    submit = SubmitField('Submit')