"""Represent an idea entity."""

from glossary import db
from glossary.models.entity.entity import Entity


class Idea(Entity):

    __tablename__ = 'idea'

    __mapper_args__ = {
        'polymorphic_identity': 'idea',
    }

    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                          primary_key=True)
    title     = db.Column(db.String(255))