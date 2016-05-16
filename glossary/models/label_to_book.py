"""Represent a many-to-many relationship between labels and books."""

from glossary import db


labels = db.Column('label_fk', db.Integer, db.ForeignKey('label.id'))
books = db.Column('book_fk', db.Integer, db.ForeignKey('book.id'))
label_to_book = db.Table('label_to_book', db.metadata, labels, books)
