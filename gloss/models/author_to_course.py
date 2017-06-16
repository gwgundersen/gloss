"""Represent a many-to-many relationship between authors and courses."""

from gloss import db


authors = db.Column('author_fk', db.Integer, db.ForeignKey('author.id'))
courses = db.Column('course_fk', db.Integer, db.ForeignKey('course.entity_fk'))
author_to_course = db.Table('author_to_course', db.metadata, authors, courses)
