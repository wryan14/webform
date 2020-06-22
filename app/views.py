from app import app, dapp
from flask import render_template, redirect, url_for, session, request
from .forms import NewPublication, UpdatePublication, UpdatePublicationStatus
from .utility import crossref_lookup, cdm_pull
import flask
import json

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
    if name != '':
        form.name.data = name

    if doi != '':
        form.doi.data = doi

    if 'doifind' not in request.form:
        if form.validate_on_submit():
            print(form.doi.data, 1)
            session['doi'] = form.doi.data
            session['name'] = form.name.data

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
        name=json.loads(flask.session['data'])
        name = name['Title']['0']
        print(name)
    except KeyError:
        name = None
    

    form = UpdatePublication()
    form.name.data = name

    if form.validate_on_submit():

        name = form.name.data
        form.name.data = ''
        return redirect(url_for('success_edit'))

    return render_template('editpub.html', form=form, name=name)


@app.route('/update', methods=['GET', 'POST'])
def updatepub():
    '''Renders new publication web-form'''

    name = False
    form = UpdatePublicationStatus()

    if form.validate_on_submit():

        name = form.name.data
        form.name.data = ''
        return redirect(url_for('success_update'))

    return render_template('updatepub.html', form=form, name=name)


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