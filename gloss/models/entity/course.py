"""Represent a course entity."""

from gloss import db
from gloss.models.entity.entity import Entity


class Course(Entity):

    __tablename__ = 'course'

    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                          primary_key=True)
    title     = db.Column(db.String(255), nullable=False)
    url       = db.Column(db.String(255), nullable=True)
    year      = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'course',
    }
