"""Represent a many-to-many relationship between authors and talks."""

from glossary import db


authors = db.Column('author_fk', db.Integer, db.ForeignKey('author.id'))
talks = db.Column('talk_fk', db.Integer, db.ForeignKey('talk.entity_fk'))
author_to_talk = db.Table('author_to_talk', db.metadata, authors, talks)
