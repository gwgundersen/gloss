"""Represent a many-to-many relationship between labels and talks."""

from glossary import db


labels = db.Column('label_fk', db.Integer, db.ForeignKey('label.id'))
talks = db.Column('talk_fk', db.Integer, db.ForeignKey('talk.entity_fk'))
label_to_talk = db.Table('label_to_talk', db.metadata, labels, talks)
