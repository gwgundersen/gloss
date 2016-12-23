"""Represent a gloss annotating an entity."""

from flask.ext.login import current_user

from glossary import db


class Gloss(db.Model):

    __tablename__ = 'gloss'
    id        = db.Column(db.Integer, primary_key=True)
    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                           nullable=True)
    text_     = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    archive   = db.Column(db.Boolean, nullable=False, default=False)
    labels    = db.relationship('Label', backref='glosses',
                                 secondary='label_to_gloss')
    is_private = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def text(self):
        if current_user.is_authenticated:
            return self.text_
        return None

    @property
    def endpoint(self):
        return 'gloss'

    @property
    def labels_alpha(self):
        return sorted(self.labels, key=lambda x: x.name)
