"""Represent a scientific publication."""

from glossary import db
from entity import Entity


class Paper(Entity):

    __tablename__ = 'paper'
    id = db.Column(db.Integer, db.ForeignKey('entity.id'), primary_key=True)
    title = db.Column(db.String(255))
    labels = db.relationship('Label', backref='papers',
                             secondary='label_to_paper')

    __mapper_args__ = {
        'polymorphic_identity': 'paper',
    }

    def __init__(self):
        pass

    @property
    def first_author(self):
        return self.authors[0]

    @property
    def last_author(self):
        return self.authors[-1]

    @property
    def endpoint(self):
        return 'paper'
