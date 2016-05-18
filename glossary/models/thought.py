"""Represent a thought gloss."""

from gloss import Gloss


class Thought(Gloss):

    __mapper_args__ = {
        'polymorphic_identity': 'thought',
    }
