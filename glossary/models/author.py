"""Represent an author of a paper, book, talk, etc."""

from glossary import db


class Author(db.Model):

    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    papers = db.relationship('Paper', backref='authors',
                             secondary='author_to_paper')
    books = db.relationship('Book', backref='authors',
                            secondary='author_to_book')

    def __init__(self):
        pass

    @property
    def name_as_url(self):
        return '%s_%s' % (self.first_name, self.last_name)

    @property
    def endpoint(self):
        return 'author'

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
