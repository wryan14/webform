from app import app, dapp, db  
from .models import Doc, Author
from flask import render_template, redirect, url_for, session, request
from .forms import NewPublication, UpdatePublication, UpdatePublicationStatus
from .utility import CRef, cdm_pull
import flask
import json

@app.route('/')
def home():
    '''Welcome page with three option dropdown'''
    return render_template('welcome_page.html')


@app.route('/new', methods=['GET', 'POST'])
def newpub():
    '''Renders new publication web-form'''
    
    title = ''
    doi = ''
    publisher = ''
    publication = ''
    year = ''
 

    if 'doifind' in request.form:
        doi = request.form['doifind']
        try:
            cr = CRef(doi)
            title = cr.title
            publisher = cr.publisher 
            publication = cr.journal_name 
            year = str(cr.year)

        except TypeError:
            pass

    form = NewPublication()
    if title != '':
        form.title.data = title

    if doi != '':
        form.doi.data = doi
    
    if publisher != '':
        form.publisher.data = publisher
    
    if publication != '':
        form.publication.data = publication  
    
    if year != '':
        form.year.data = year  

    if 'doifind' not in request.form:
        if form.validate_on_submit():
            print(form.doi.data, 1)
            session['doi'] = form.doi.data
            session['title'] = form.title.data
            session['publisher'] = form.publisher.data  
            session['publication'] = form.publication.data  
            session['year'] = form.year.data 

            new_doc = Doc()
            db.session.add(new_doc)
            for author in form.authors.data:
                new_author = Author(**author)

                #  add to doc database entry
                new_doc.authors.append(new_author)
            new_doc.title = form.title.data  
            db.session.commit()  

            return redirect(url_for('success_new'))

    return render_template('newpub.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
def editpub():
    '''Renders new publication web-form'''
    # load data using cdm_pull and search existing data
    if 'cdmlookup' in request.form: # cdmlookup is the lookup form on editpub.html
        query = request.form['cdmlookup']
        df = cdm_pull('argument not yet needed')
        filtered = df[df.apply(lambda row: row.astype(str).str.contains(query).any(), axis=1)]
        
        
    try:
        title=json.loads(flask.session['data'])
        title = title['Title']['0']
    except KeyError:
        title = None
    

    form = UpdatePublication()
    form.title.data = title

    if form.validate_on_submit():

        title = form.title.data
        form.title.data = ''
        return redirect(url_for('success_edit'))

    return render_template('editpub.html', form=form, title=title)


@app.route('/update', methods=['GET', 'POST'])
def updatepub():
    '''Renders new publication web-form'''

    title = False
    form = UpdatePublicationStatus()

    if form.validate_on_submit():

        title = form.title.data
        form.title.data = ''
        return redirect(url_for('success_update'))

    return render_template('updatepub.html', form=form, title=title)


@app.route('/success_new')
def success_new():
    '''Confirmation page after form submission for new items'''
    return render_template('success_new.html')

@app.route('/success_edit')
def success_edit():
    '''Confirmation page after form submission for edit items'''
    return render_template('success_edit.html')

@app.route('/success_update')
def success_update():
    '''Confirmation page after form submission for update item'''
    return render_template('success_update.html')


@app.route("/edit_table", methods=['GET', 'POST'])
def dash_app():

    if 'edittable' in request.form:
        return render_template('editpub')

    return dapp.index()