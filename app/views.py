from app import app, dapp, db  
from .models import Doc, Author, EditDoc, BeforeDoc, BeforeAuthor, EditAuthor
from flask import render_template, redirect, url_for, session, request
from .forms import NewPublication, UpdatePublication, UpdatePublicationStatus
from .utility import CRef, cdm_pull
from sqlalchemy import text 
import flask
import json
import datetime
import pandas as pd 

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

    title = ''
    doi = ''
    publication = ''
    authors = ''
    lname = ''
    fname = '' 

    try:
        new_doc = EditDoc()
        before_doc = BeforeDoc() 
        db.session.add(new_doc)
        dash_data=json.loads(flask.session['data'])
        title = dash_data['Title']['0']
        doi = dash_data['DOI_Number']['0']
        publication = dash_data['Published in']['0']
        authors = dash_data['Creator']['0']
        before_doc.title = title 
        before_doc.publication = publication
        before_doc.doi = doi
        new_doc.before_docs.append(before_doc)
        db.session.commit()  # This could potentially end up storing too much data in the database
        # Is the solution to develop a script that periodically deletes null values from the SQLite database?
        flask.session.clear()
    except KeyError:
        pass

    
    form = UpdatePublication()

    if title!='':
        form.title.data = title
    if doi!='':
        form.doi.data = doi 
    if publication!='':
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
    if 'doifind' not in request.form:
        if form.validate_on_submit():
            new_doc = db.session.query(EditDoc).order_by(EditDoc.id.desc()).first()
            new_doc = new_doc.query.get(new_doc.id-1) # may not be the best way, but this edits the last created record


            for author in form.authors.data:
                new_authors = EditAuthor(**author)  
                # add to doc database entry 
                new_doc.edit_authors.append(new_authors)

            new_doc.title = form.title.data 
            new_doc.doi = form.doi.data.strip('https://doi.org/').strip('http://doi.org/')
            new_doc.publication = form.publication.data   
            new_doc.date_added = datetime.datetime.now() 

            db.session.commit()
            
            # store data for success page from database     
            sql = text('''
                SELECT edit_docs.id, before_docs.title, edit_docs.title, 
                before_docs.doi, edit_docs.doi, 
                before_docs.publication, edit_docs.publication
                FROM before_docs 
                INNER JOIN edit_docs ON before_docs.doc_id=edit_docs.id;
            ''')
            results= db.engine.execute(sql)
            data = [row for row in results]
            columns = ['Id', 'Title-Before', 'Title-After', 'DOI-Before', 'DOI-After', 'Publication-Before', 'Publication-After']

            df = pd.DataFrame(columns=columns, data=data)


            df = df[df['Id']==new_doc.id]
            
            # assign session values
            for idx, row in df.iterrows():
                if row['Title-Before']!=row['Title-After']:
                    session['Title-Before'] = row['Title-Before']
                    session['Title-After'] = row['Title-After']
                else:
                    session['Title-Before'] = None  
                    session['Title-After'] = None
                if row['DOI-Before'] != row['DOI-After']:
                    session['DOI-Before'] = row['DOI-Before']
                    session['DOI-After'] = row['DOI-After']
                else:
                    session['DOI-Before'] = None  
                    session['DOI-After'] = None 
                if row['Publication-Before'] != row['Publication-After']:
                    session['Publication-Before'] = row['Publication-Before']
                    session['Publication-After'] = row['Publication-After']
                else:
                    session['Publication-Before'] = None 
                    session['Publication-After'] = None





  
           
            

            # session['Title-Before'] = 
            # session['Title-After'] = db_results.title
            # session['Doi'] = db_results.doi 



            return redirect(url_for('success_edit'))
    edit_docs = EditDoc.query
    return render_template('editpub.html', form=form)

    


@app.route('/update', methods=['GET', 'POST'])
def updatepub():
    '''Renders new publication web-form'''

    title = False
    form = UpdatePublicationStatus()

    if form.validate_on_submit():

        title = form.title.data
        print(title)
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