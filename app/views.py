from app import app, dapp, db  
from .models import Doc, Author, EditDoc, BeforeDoc, BeforeAuthor, EditAuthor
from flask import render_template, redirect, url_for, session, request
from .forms import NewPublication, UpdatePublication, UpdatePublicationStatus
from .utility import CRef, cdm_pull
import flask
import json
import datetime

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
    authors = ''
    lname = ''
    fname = ''
 

    if 'doifind' in request.form:
        doi = request.form['doifind']
        try:
            cr = CRef(doi)
            title = cr.title
            publisher = cr.publisher 
            publication = cr.journal_name 
            year = str(cr.year)
            authors = cr.author_list

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
    
    if authors != '':
        for idx, auth_name in enumerate(authors):
            lname = auth_name.split(',')[0].strip()
            fname = auth_name.split(',')[1].strip()

            if idx == 0:
                form.authors[idx].first_name.data = fname 
                form.authors[idx].last_name.data = lname
            else:
                form.authors.append_entry()
                form.authors[idx].first_name.data = fname 
                form.authors[idx].last_name.data = lname

    if 'doifind' not in request.form:
        if form.validate_on_submit():            
            new_doc = Doc()
            db.session.add(new_doc)
            for author in form.authors.data:
                new_author = Author(**author)
                #  add to doc database entry
                new_doc.authors.append(new_author)
            
            new_doc.title = form.title.data
            new_doc.doi = form.doi.data.strip('https://doi.org/').strip('http://doi.org/')
            new_doc.publisher = form.publisher.data 
            new_doc.publication = form.publication.data
            new_doc.publication_year = form.year.data 
            new_doc.date_added = datetime.datetime.now()
        
            db.session.commit()  
            
            db_results = Doc.query.get(new_doc.id)
            print(db_results)
            session['Title'] = db_results.title
            session['Doi'] = db_results.doi 
            
            authors = Author.query.filter_by(doc_id=new_doc.id)
            author_list = [(x.first_name, x.last_name) for x in authors.all()]
            session['Author_list'] = author_list

            session['Publication'] = db_results.publication
            session['Publisher'] = db_results.publisher 


            return redirect(url_for('success_new'))
    docs = Doc.query
    return render_template('newpub.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
def editpub():
    '''Renders new publication web-form'''
    try:
        dash_data=json.loads(flask.session['data'])
        title = dash_data['Title']['0']
        doi = dash_data['DOI_Number']['0']
        publication = dash_data['Published in']['0']
        authors = dash_data['Creator']['0']

    except KeyError:
        title = None
        doi = None
        publication = None
        authors = ''
    
    form = UpdatePublication()
    form.title.data = title
    form.doi.data = doi
    form.publication.data = publication

    if authors != '':
        for idx, auth_name in enumerate(authors.split(';')):
            lname = auth_name.split(',')[0].strip()
            fname = auth_name.split(',')[1].strip()

            if idx == 0:
                form.authors[idx].first_name.data = fname 
                form.authors[idx].last_name.data = lname
            else:
                form.authors.append_entry()
                form.authors[idx].first_name.data = fname 
                form.authors[idx].last_name.data = lname

    if form.validate_on_submit():

        new_doc = EditDoc()
        before_docs = BeforeDoc() 
        db.session.add(new_doc)


        # Gather data from table first (before)
        if authors != '':
            for idx, auth_name in enumerate(authors.split(';')):
                lname = auth_name.split(',')[0].strip()
                fname = auth_name.split(',')[1].strip()
                author_entry = {'first_name': fname, 'last_name': lname}
                new_author = BeforeAuthor(**author_entry)
                before_docs.before_authors.append(new_author)
        before_docs.title = title
        before_docs.doi = doi 
        before_docs.publication = publication  

        new_doc.title = form.title.data 
        new_doc.doi = form.doi.data 
        new_doc.publication = form.publication.data 
        print(form.title.data)
      
        for edit_author in form.authors.data:
            new_edit_author = EditAuthor(**edit_author)
            new_doc.edit_authors.append(new_edit_author)
        
        new_doc.before_docs.append(before_docs)
        new_doc.date_added = datetime.datetime.now()
        
        db.session.commit()

        # query data and add to session for success page
        db_results = EditDoc.query.get(new_doc.id)
        print(db_results)
        session['Title-Before'] = db_results.title
        session['Title-After'] = db_results.title
        session['Doi-Before'] = db_results.doi
        session['Doi-After'] = db_results.doi
        session['Publication-Before'] = db_results.publication
        session['Publication-After'] = db_results.publication 

        authors_before = EditAuthor.query.filter_by(doc_id=new_doc.id) 
        author_before_list = [(x.first_name, x.last_name) for x in authors_before.all() ]

        authors_after = EditAuthor.query.filter_by(doc_id=new_doc.id) 
        author_after_list = [(x.first_name, x.last_name) for x in authors_after.all()]

        session['Author_list_before'] = author_before_list  
        session['Author_list_after'] = author_after_list  


        
        return redirect(url_for('success_edit'))
    edit_docs = EditDoc.query
    return render_template('editpub.html', form=form, title=title, 
                                            doi=doi, publication=publication)


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