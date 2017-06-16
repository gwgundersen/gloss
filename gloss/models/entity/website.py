"""Represent a website entity."""

from gloss import db
from gloss.models.entity.entity import Entity


class Website(Entity):

    __tablename__ = 'website'

    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                          primary_key=True)
    title     = db.Column(db.String(255))
    url       = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)

    __mapper_args__ = {
        'polymorphic_identity': 'website',
    }
