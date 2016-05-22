"""Represent a many-to-many relationship between labels and glosses."""

from glossary import db


labels = db.Column('label_fk', db.Integer, db.ForeignKey('label.id'))
glosses = db.Column('gloss_fk', db.Integer, db.ForeignKey('gloss.id'))
label_to_gloss = db.Table('label_to_gloss', db.metadata, labels, glosses)
