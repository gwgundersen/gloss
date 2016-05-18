"""Represent a non-hierarchical keyword tag."""

from glossary import db


class Label(db.Model):

    __tablename__ = 'label'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    endpoint = 'label'
