"""Represent a talk, presentation, course lecture, etc."""

from gloss import db
from gloss.models.entity.entity import Entity


class Talk(Entity):

    __tablename__ = 'talk'
    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                            primary_key=True)
    title     = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    location  = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'talk',
    }
