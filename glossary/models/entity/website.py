"""Represent a website entity."""

from glossary import db
from glossary.models.entity.entity import Entity


class Website(Entity):

    __tablename__ = 'website'

    __mapper_args__ = {
        'polymorphic_identity': 'website',
    }

    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                          primary_key=True)
    title     = db.Column(db.String(255))
    url       = db.Column(db.String(255))
