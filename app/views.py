from app import app
from flask import render_template, redirect, url_for
from .forms import *

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
        return redirect(url_for('success'))
    
    return render_template('newpub.html', form=form, name=name)  

@app.route('/edit', methods=['GET', 'POST'])
def editpub():
    '''Renders new publication web-form'''

    name = False
    form = NewPublication()

    if form.validate_on_submit():

        name = form.name.data  
        form.name.data = ''
        return redirect(url_for('success'))
    
    return render_template('editpub.html', form=form, name=name)  

@app.route('/update', methods=['GET', 'POST'])
def updatepub():
    '''Renders new publication web-form'''

    name = False
    form = NewPublication()

    if form.validate_on_submit():

        name = form.name.data  
        form.name.data = ''
        return redirect(url_for('success'))
    
    return render_template('updatepub.html', form=form, name=name)  


@app.route('/success')
def success():
    '''Confirmation page after form submission'''
    return render_template('success.html')
