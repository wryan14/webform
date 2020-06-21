from app import app
from flask import render_template, redirect, url_for, session, request
from .forms import *
from .utility import crossref_lookup

@app.route('/')
def home():
    '''Welcome page with three option dropdown'''
    return render_template('welcome_page.html')


@app.route('/new', methods=['GET', 'POST'])
def newpub():
    '''Renders new publication web-form'''
    name = ''
    doi = ''
    if 'doifind' in request.form:
        doi = request.form['doifind']
        try:
            name = crossref_lookup(doi, 'title')[0]
            # make sure full url was not included
            name.replace('https://doi.org', '').replace('http://doi.org', '')
        except TypeError:
            pass

    form = NewPublication()
    if name!='':
        form.name.data= name
    
    if doi!='':
        form.doi.data = doi
    
    if 'doifind' not in request.form:
        if form.validate_on_submit():
            print(form.doi.data, 1)
            session['doi'] = form.doi.data
            session['name'] = form.name.data

            return redirect(url_for('success'))
    
    return render_template('newpub.html', form=form)  

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
