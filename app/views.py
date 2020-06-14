from app import app
from flask import render_template
from forms import *

@app.route('/')
def home():
    '''Welcome page with three option dropdown'''
    return render_template('welcome_page.html')

@app.route('/new', methods=['GET', 'POST'])
def newpub():
    '''Renders new publication web-form'''

    name = False
    form = NewPublication()

    if form.validate_on_submit():

        name = form.name.data  
        form.name.data = ''
    
    return render_template('newpub.html', form=form, name=name)  
    
