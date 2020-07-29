# models.py
# This document contains all of the models required to store data in a SQLite database.
# Dynamic author fields heavily borrows from https://www.rmedgar.com/blog/dynamic-fields-flask-wtf

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # start database

########################
# New Pubs Model
########################


class Doc(db.Model):
    """Model associated with adding a new publication.

    :param id: primary key (auto-generated)
    :type id: int 
    :param date_added: date document added to database (useful for queries; auto-generated)
    :type date_added: datetime
    :param title: title of new document 
    :type title: str
    :param doi: Digitial Object Identifier (DOI), should not contain https://doi.org/
    :type doi: str
    :param publisher: Name of entity publishing new object
    :type publisher: str 
    :param publication: Name of entity in which object is published
    :type publication: str
    :param publication_year: Year entity published (different from date_added)
    :type publication_year: str
    """
    __tablename__ = 'docs'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime)
    title = db.Column(db.String(1000))
    doi = db.Column(db.String(100))
    publisher = db.Column(db.String(1000))
    publication = db.Column(db.String(1000))
    publication_year = db.Column(db.String(4))


class Author(db.Model):
    """Author information associated with Doc model and adding new publication.

    :param id: primary key (auto-generated)
    :type id: int
    :param doc_id: foreign key from Doc model (Doc.id)
    :type doc_id: int
    :param first_name: First name of author associated with Doc.id publication
    :type first_name: str
    :param last_name: Last name of author associated with Doc.id publication
    :type last_name: str
    :param doc: Establishes backref connection to Doc model
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('docs.id'))

    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(500))

    # Relationship
    doc = db.relationship(
        'Doc',
        backref=db.backref('authors', lazy='dynamic', collection_class=list)
    )

########################
# Edit Pubs Model
########################


class BeforeDoc(db.Model):
    """Model that captures state of a document object's metadata prior to edits.  This will be a useful
    point of comparison for later work with document metadata. (i.e. What did the user edit?)

    :param id: primary key (auto-generated)
    :type id: int
    :param doc_id: foreign key for the EditDoc model, edit_docs.id
    :type doc_id: int 
    :param title: title of document prior to edits
    :type title: str
    :param doi: Digital object identifier (DOI) prior to edits 
    :type doi: str 
    :param publication: Entitiy publishing document object prior to edits
    :type publication: str 
    :param edit_doc: Establishes backref connection to EditDoc model
    """
    __tablename__ = 'before_docs'
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('edit_docs.id'))

    title = db.Column(db.String(1000))
    doi = db.Column(db.String(100))
    publication = db.Column(db.String(1000))

    edit_doc = db.relationship(
        'EditDoc',
        backref=db.backref('before_docs', lazy='dynamic',
                           collection_class=list)
    )


class BeforeAuthor(db.Model):
    """Authors associated with BeforeDoc documents (i.e. documents prior to edits).

    :param id: primary key (auto generated)
    :type id: int 
    :param doc_id: foreign key for BeforeDoc model 
    :type doc_id: int 
    :param first_name: first name associated with document author prior to edits 
    :type first_name: str 
    :param last_name: last name associated with document author prior to edits 
    :type last_name: str 
    :param before_doc: Establishes backref connection to BeforeDoc
    """
    __tablename__ = "before_authors"
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('before_docs.id'))

    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(500))

    # Relationsip
    before_doc = db.relationship(
        'BeforeDoc',
        backref=db.backref('before_authors', lazy='dynamic',
                           collection_class=list)
    )


class EditDoc(db.Model):
    """Model that captures the state of a document after a user submits edits.  Changes
    can later be identified by comparing EditDoc metadata to BeforeDoc metadata. 

    :param id: primary key (auto-generated)
    :type id: int
    :param date_added: date document added to database (useful for queries; auto-generated)
    :type date_added: datetime 
    :param title: title of document after edits 
    :type title: str 
    :param doi: Digital Object Identifier after edits
    :type doi: str 
    :param publication: Name of entity in which document is published after edits 
    :type publication: str 
    """
    __tablename__ = 'edit_docs'
    id = db.Column(db.Integer, primary_key=True)

    date_added = db.Column(db.DateTime)
    title = db.Column(db.String(1000))
    doi = db.Column(db.String(100))
    publication = db.Column(db.String(1000))


class EditAuthor(db.Model):
    """Authors associated with EditDoc model (i.e. authors after user edits)

    :param id: primary key (auto-generated)
    :type id: int 
    :param doc_id: foreign key for EditDoc model 
    :type doc_id: int 
    :param first_name: first name associated with document author after user edits 
    :type first_name: str 
    :param last_name: last name associated with document author after user edits 
    :type last_name: str 
    :param before_doc: Establishes backref connection to EditDoc
    """
    __tablename__ = "edit_authors"
    id = db.Column(db.Integer, primary_key=True)

    doc_id = db.Column(db.Integer, db.ForeignKey('edit_docs.id'))

    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(500))

    # Relationsip
    edit_doc = db.relationship(
        'EditDoc',
        backref=db.backref('edit_authors', lazy='dynamic',
                           collection_class=list)
    )
