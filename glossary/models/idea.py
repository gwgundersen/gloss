"""Represent an idea entity."""

from glossary import db
from entity import Entity


class Idea(Entity):

    __tablename__ = 'idea'

    __mapper_args__ = {
        'polymorphic_identity': 'idea',
    }

    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                          primary_key=True)
    name      = db.Column(db.String(255))
    url       = db.Column(db.String(255))

    @property
    def endpoint(self):
        return 'entity/idea'
