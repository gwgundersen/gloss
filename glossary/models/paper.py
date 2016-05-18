"""Represent a scientific publication."""

from glossary import db
from entity import Entity


class Paper(Entity):

    __tablename__ = 'paper'
    id           = db.Column(db.Integer, db.ForeignKey('entity.id'), primary_key=True)
    title        = db.Column(db.String(255))
    reason       = db.Column(db.String(255))
    date_read    = db.Column(db.Date)
    depth        = db.Column(db.Integer)
    year         = db.Column(db.Integer)
    min_required = db.Column(db.Float)
    labels       = db.relationship('Label', backref='papers',
                                   secondary='label_to_paper')
    journal_fk   = db.Column('journal_fk', db.Integer, db.ForeignKey('journal.id'))
    journal      = db.relationship('Journal', backref='papers')

    __mapper_args__ = {
        'polymorphic_identity': 'paper',
    }

    @property
    def first_author(self):
        return self.authors[0]

    @property
    def last_author(self):
        return self.authors[-1]

    @property
    def endpoint(self):
        return 'entity/paper'
