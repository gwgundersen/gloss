"""Represent a scientific publication."""

from glossary import db
from entity import Entity


class Book(Entity):

    __tablename__ = 'book'
    id = db.Column(db.Integer, db.ForeignKey('entity.id'), primary_key=True)
    title = db.Column(db.String(255))
    #reason = db.Column(db.String(255))
    #pages = db.Column(db.Integer)
    #year = db.Column(db.Integer)
    labels = db.relationship('Label', backref='books',
                             secondary='label_to_book')

    __mapper_args__ = {
        'polymorphic_identity': 'book',
    }

    def __init__(self):
        pass

    @property
    def author_info(self):
        a = self.authors[0]
        if len(self.authors) > 1:
            return '%s et al' % a.last_name
        return '%s %s' % (a.first_name, a.last_name)
