"""Represent an annotatable entity in the program."""

from glossary import db


class Entity(db.Model):

    __tablename__ = 'entity'
    id = db.Column(db.Integer, primary_key=True)
    type_ = db.Column(db.String(255))
    glosses = db.relationship('Gloss', backref='entity',
                              order_by='desc(Gloss.timestamp)')

    __mapper_args__ = {
        'polymorphic_identity': 'entity',
        'polymorphic_on': type_
    }
