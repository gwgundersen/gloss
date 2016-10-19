"""Represent a gloss annotating an entity."""

from flask.ext.login import current_user

from glossary import db


class Gloss(db.Model):

    __tablename__ = 'gloss'
    id         = db.Column(db.Integer, primary_key=True)
    type_      = db.Column(db.String(50))
    entity_fk  = db.Column(db.Integer, db.ForeignKey('entity.id'),
                           nullable=True)
    text_      = db.Column(db.Text)
    timestamp  = db.Column(db.DateTime)
    archive    = db.Column(db.Boolean, nullable=False, default=False)
    _labels    = db.relationship('Label', backref='glosses',
                                 secondary='label_to_gloss')
    is_private = db.Column(db.Boolean, nullable=False, default=True)

    __mapper_args__ = {
        'polymorphic_identity': 'gloss',
        'polymorphic_on': type_
    }

    @property
    def text(self):
        if current_user.is_authenticated:
            return self.text_
        return None

    @property
    def endpoint(self):
        return 'gloss'

    @property
    def labels(self):
        return sorted(self._labels, key=lambda x: x.name)


class Question(Gloss):

    __mapper_args__ = {
        'polymorphic_identity': 'question',
    }


class Summary(Gloss):

    __mapper_args__ = {
        'polymorphic_identity': 'summary',
    }


class Thought(Gloss):

    __mapper_args__ = {
        'polymorphic_identity': 'thought',
    }


class Todo(Gloss):

    __mapper_args__ = {
        'polymorphic_identity': 'todo',
    }
