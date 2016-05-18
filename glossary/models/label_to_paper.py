"""Represent a many-to-many relationship between labels and papers."""

from glossary import db


labels = db.Column('label_fk', db.Integer, db.ForeignKey('label.id'))
papers = db.Column('paper_fk', db.Integer, db.ForeignKey('paper.entity_fk'))
label_to_paper = db.Table('label_to_paper', db.metadata, labels, papers)
