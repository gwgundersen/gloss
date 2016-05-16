"""Represent a many-to-many relationship between authors and papers."""

from glossary import db


authors = db.Column('author_fk', db.Integer, db.ForeignKey('author.id'))
books = db.Column('book_fk', db.Integer, db.ForeignKey('book.id'))
author_to_book = db.Table('author_to_book', db.metadata, authors, books)
