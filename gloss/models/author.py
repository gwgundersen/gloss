"""Represent an author of a paper, book, talk, etc."""

from gloss import db


class Author(db.Model):

    __tablename__ = 'author'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255))
    is_female   = db.Column(db.Boolean)
    is_poc      = db.Column(db.Boolean)
    nationality = db.Column(db.String(255))

    books  = db.relationship('Book', backref='authors',
                             secondary='author_to_book')
    papers = db.relationship('Paper', backref='authors',
                             secondary='author_to_paper')
    talks  = db.relationship('Talk', backref='authors',
                             secondary='author_to_talk')

    @property
    def endpoint(self):
        return 'author/%s' % self.id
