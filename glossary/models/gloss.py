"""Represent a gloss annotating an entity."""

from glossary import db


class Gloss(db.Model):

    __tablename__ = 'gloss'
    id = db.Column(db.Integer, primary_key=True)
    type_ = db.Column(db.String(50))
    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                          nullable=True)
    text_ = db.Column(db.Text)
    endpoint = 'gloss'

    __mapper_args__ = {
        'polymorphic_identity': 'gloss',
        'polymorphic_on': type_
    }
