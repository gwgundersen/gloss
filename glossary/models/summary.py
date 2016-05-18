"""Represent a summary gloss such as quotes, paraphrases, and outlines."""

from glossary import db
from gloss import Gloss


class Summary(Gloss):

    __mapper_args__ = {
        'polymorphic_identity': 'summary',
    }
