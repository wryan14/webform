from flask_sqlalchemy import SQLAlchemy 

# Dynamic author fields heavily borrows from https://www.rmedgar.com/blog/dynamic-fields-flask-wtf

db = SQLAlchemy()

class Doc(db.Model):
    """Stores docs."""
    __tablename__ = 'docs'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime)
    title = db.Column(db.String(1000))
    doi = db.Column(db.String(100))
    publisher = db.Column(db.String(1000))
    publication = db.Column(db.String(1000))
    publication_year = db.Column(db.String(4))


class Author(db.Model):
    """Stores authors of a doc."""
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

class EditDoc(db.Model):
    """Stores docs for edit"""
    __tablename__='edit_docs'
    id = db.Column(db.Integer, primary_key=True) 
    date_added = db.Column(db.DateTime)
    title_before = db.Column(db.String(1000))
    doi_before = db.Column(db.String(100))
    publication_before = db.Column(db.String(1000))

    title_after = db.Column(db.String(1000))
    doi_after = db.Column(db.String(100))
    publication_after = db.Column(db.String(1000))


class BeforeAuthor(db.Model):
    '''Stores author of edit doc'''
    __tablename__="before_authors"
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('edit_docs.id'))

    first_name_before = db.Column(db.String(300))
    last_name_before = db.Column(db.String(500))


    # Relationsip
    edit_doc = db.relationship(
        'EditDoc',
        backref=db.backref('before_authors', lazy='dynamic', collection_class=list)
    )

class EditAuthor(db.Model):
    '''Stores author of edit doc'''
    __tablename__="edit_authors"
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('edit_docs.id'))

    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(500))

    # Relationsip
    edit_doc = db.relationship(
        'EditDoc',
        backref=db.backref('edit_authors', lazy='dynamic', collection_class=list)
    )