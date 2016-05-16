"""Represent an idea gloss."""

from glossary import db
from gloss import Gloss


class Idea(Gloss):

    __mapper_args__ = {
        'polymorphic_identity': 'idea',
    }

    def __init__(self):
        pass
