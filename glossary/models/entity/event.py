"""Represent an event entity."""

from glossary import db
from glossary.models.entity.entity import Entity


class Event(Entity):

    __tablename__ = 'event'

    __mapper_args__ = {
        'polymorphic_identity': 'event',
    }

    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                          primary_key=True)
    title     = db.Column(db.String(255))
