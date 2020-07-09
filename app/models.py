from flask_sqlalchemy import SQLAlchemy 

# Dynamic author fields heavily borrows from https://www.rmedgar.com/blog/dynamic-fields-flask-wtf

db = SQLAlchemy()

class Doc(db.Model):
    """Stores docs."""
    __tablename__ = 'docs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))


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