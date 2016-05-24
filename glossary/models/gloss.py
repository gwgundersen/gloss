"""Represent a gloss annotating an entity."""

from glossary import db


class Gloss(db.Model):

    __tablename__ = 'gloss'
    id        = db.Column(db.Integer, primary_key=True)
    type_     = db.Column(db.String(50))
    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                          nullable=True)
    text_     = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    archive   = db.Column(db.Boolean, nullable=False, default=False)
    labels    = db.relationship('Label', backref='glosses',
                                secondary='label_to_gloss')

    __mapper_args__ = {
        'polymorphic_identity': 'gloss',
        'polymorphic_on': type_
    }

    @property
    def endpoint(self):
        return 'gloss'


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


class Blog(Gloss):

    __mapper_args__ = {
        'polymorphic_identity': 'blog',
    }
