"""Represent an author of a paper, book, talk, etc."""

from glossary import db


class Author(db.Model):

    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    papers = db.relationship('Paper', backref='authors',
                             secondary='author_to_paper')

    def __init__(self):
        pass
