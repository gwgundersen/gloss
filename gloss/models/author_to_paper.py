"""Represent a many-to-many relationship between authors and papers."""

from gloss import db


authors = db.Column('author_fk', db.Integer, db.ForeignKey('author.id'))
papers = db.Column('paper_fk', db.Integer, db.ForeignKey('paper.entity_fk'))
author_to_paper = db.Table('author_to_paper', db.metadata, authors, papers)
