"""Represent a many-to-many relationship between authors and websites."""

from gloss import db


authors = db.Column('author_fk', db.Integer, db.ForeignKey('author.id'))
websites = db.Column('website_fk', db.Integer, db.ForeignKey('website.entity_fk'))
author_to_website = db.Table('author_to_website', db.metadata, authors, websites)
