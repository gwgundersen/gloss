"""Represent a many-to-many relationship between labels and ideas."""

from glossary import db


labels = db.Column('label_fk', db.Integer, db.ForeignKey('label.id'))
ideas = db.Column('idea_fk', db.Integer, db.ForeignKey('idea.entity_fk'))
label_to_idea = db.Table('label_to_idea', db.metadata, labels, ideas)
