# views.py
# views establish the structure and navigation of the webform.

from app import app, dapp, db
from .models import Doc, Author, EditDoc, BeforeDoc, BeforeAuthor, EditAuthor
from flask import render_template, redirect, url_for, session, request
from .forms import NewPublication, UpdatePublication, UpdatePublicationStatus
from .utility import CRef, cdm_pull
import flask
import json
import datetime
import pandas as pd


@app.route('/')
def home():
    """Welcome page that provides options to navigate to new, edit, or forthcoming
    functionality.

    Returns:
        ./templates/welcome_page.html
    """
    return render_template('welcome_page.html')


@app.route('/new', methods=['GET', 'POST'])
def newpub():
    """New publication page where users can fill in the NewPublication form,
    and save form to Doc database table. 

    Returns:
        ./templates/newpub.html
        ./templates/success_new.html (upon submit)
    """
    # initial variables should exist, but contain an empty string
    title = ''
    doi = ''
    publisher = ''
    publication = ''
    year = ''
    authors = ''
    lname = ''
    fname = ''

    if 'doifind' in request.form:   # run utilities.CRef function when user submits doifind form
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

    form = NewPublication() # create form

    # if utilities.CRef successfully parses the DOI, replace the empty form field with parsed content
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

    if 'doifind' not in request.form:   # needed to make a distinction between new form and doifind
        if form.validate_on_submit():
            new_doc = Doc() # call database model
            db.session.add(new_doc)
            for author in form.authors.data:
                new_author = Author(**author)
                #  add to doc database entry
                new_doc.authors.append(new_author)
            
            # transfer the submitted form data to the database model
            new_doc.title = form.title.data
            new_doc.doi = form.doi.data.strip(
                'https://doi.org/').strip('http://doi.org/')
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
    """Edit Publication page. If the users selects a table row from dash_app template, 
        this view saves the stored flask session data into the BeforeDoc database model.
        Any changes submitted to this view are then stored in the EditDoc model. 
    
        Returns:
            ./templates/editpub.html
            ./templates/success_edit.html (upon submit)
    """

    # initial variables should contain empty string
    title = ''
    doi = ''
    publication = ''
    authors = ''
    lname = ''
    fname = ''

    try:
        # EditDoc and BeforeDoc are related, so we need to create instances of both in order to store
        # the BeforeDoc state. Assuming the user selects a row, flask.session data comes from the dash tables (see __init__.py)
        new_doc = EditDoc()
        before_doc = BeforeDoc()
        db.session.add(new_doc)
        dash_data = json.loads(flask.session['data'])
        title = dash_data['Title']['0']
        doi = dash_data['DOI_Number']['0']
        publication = dash_data['Published in']['0']
        authors = dash_data['Creator']['0']

        # append authors to database
        if authors != '':
            for idx, auth_name in enumerate(authors.split(';')):
                lname = auth_name.split(',')[0].strip()
                fname = auth_name.split(',')[1].strip()

                before_author = BeforeAuthor(first_name=fname, last_name=lname)
                before_doc.before_authors.append(before_author)

        before_doc.title = title
        before_doc.publication = publication
        before_doc.doi = doi
        new_doc.before_docs.append(before_doc)
        db.session.commit()  
        flask.session.clear()
    except KeyError:
        pass

    form = UpdatePublication()

    if title != '':
        form.title.data = title
    if doi != '':
        form.doi.data = doi
    if publication != '':
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
            new_doc = db.session.query(EditDoc).order_by(
                EditDoc.id.desc()).first()
            # edits the last created record (better way?)
            new_doc = new_doc.query.get(new_doc.id-1)

            for author in form.authors.data:
                new_authors = EditAuthor(**author)
                # add to doc database entry
                new_doc.edit_authors.append(new_authors)

            new_doc.title = form.title.data
            new_doc.doi = form.doi.data.strip(
                'https://doi.org/').strip('http://doi.org/')
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
            results = db.engine.execute(sql)
            data = [row for row in results]
            columns = ['Id', 'Title-Before', 'Title-After', 'DOI-Before',
                       'DOI-After', 'Publication-Before', 'Publication-After']

            df = pd.DataFrame(columns=columns, data=data)

            df = df[df['Id'] == new_doc.id]

            # assign session values
            for idx, row in df.iterrows():
                if row['Title-Before'] != row['Title-After']:
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

            # find the edit_doc id, so we can correctly combine before authors
            find_before_doc_id = text('''
                SELECT id FROM before_docs
                WHERE doc_id={};
            '''.format(new_doc.id))

            find_before_results = db.engine.execute(find_before_doc_id)
            find_before_id = [row for row in find_before_results][0][0]

            # find authors
            edit_author_sql = text('''
                SELECT * FROM edit_authors
                WHERE doc_id={};
            '''.format(new_doc.id))

            before_author_sql = text('''
                SELECT * FROM before_authors
                WHERE doc_id={};
            '''.format(find_before_id))

            edit_author_results = db.engine.execute(edit_author_sql)
            before_author_results = db.engine.execute(before_author_sql)

            # author data
            edit_author_data = [row for row in edit_author_results]
            before_author_data = [row for row in before_author_results]

            columns = ['Id', 'DocId', 'FirstName', 'LastName']

            edit_author_df = pd.DataFrame(
                columns=columns, data=edit_author_data)
            before_author_df = pd.DataFrame(
                columns=columns, data=before_author_data)

            # combine first and last names of authors for success page
            edit_author_list = list(
                zip(edit_author_df['FirstName'].tolist(), edit_author_df['LastName'].tolist()))
            before_author_list = list(zip(
                before_author_df['FirstName'].tolist(), before_author_df['LastName'].tolist()))

            # turn list of tuples into list of strings
            edit_author_list = ['{} {}'.format(
                x[0], x[1]) for x in edit_author_list]
            before_author_list = ['{} {}'.format(
                x[0], x[1]) for x in before_author_list]

            if edit_author_list != before_author_list:
                session['Author-Before'] = before_author_list
                session['Author-After'] = edit_author_list
            else:
                session['Author-Before'] = None
                session['Author-After'] = None

            return redirect(url_for('success_edit'))
    edit_docs = EditDoc.query
    return render_template('editpub.html', form=form)


@app.route('/update', methods=['GET', 'POST'])
def updatepub():
    """Renders the forthcoming process.

    Returns:
        ./templates/updatepub.html
        ./templates/success_update.html (upon submit)

    View still in progress
    """
    title = False
    form = UpdatePublicationStatus()

    if form.validate_on_submit():

        title = form.title.data
        form.title.data = ''
        return redirect(url_for('success_update'))

    return render_template('updatepub.html', form=form, title=title)


@app.route('/clear_table', methods=['GET', 'POST'])
def cleartable():
    """Clears null values from the edit_docs database; not intended for public use.
        For an unknown reason, the database model adds a blank row in-between each
        submit. To make the database more friendly to developers, this function does 
        some cleanup. 

        Returns:
            ./templates/welcome_page.html
    """
    remove_null = text('''
        DELETE from edit_docs
        WHERE title is null;
        ''')

    db.engine.execute(remove_null)
    return redirect(url_for('home'))


@app.route('/success_new')
def success_new():
    """Confirmation page after form submission for new items"""
    return render_template('success_new.html')


@app.route('/success_edit')
def success_edit():
    """Confirmation page after form submission for edit items"""
    return render_template('success_edit.html')


@app.route('/success_update')
def success_update():
    """Confirmation page after form submission for update item"""
    return render_template('success_update.html')


@app.route("/edit_table", methods=['GET', 'POST'])
def dash_app():
    """This dash app presents a Dash table of fields that a user can select. Once selected, 
    the data is stored into the flask.session and used in the editpub process. 
    """

    if 'edittable' in request.form:
        return render_template('editpub')

    return dapp.index()
