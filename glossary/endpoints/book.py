"""Render book-related pages."""

from flask import Blueprint, render_template

from glossary import db, models
from glossary.config import config


book_blueprint = Blueprint('book',
                           __name__,
                           url_prefix='%s/book' % config.get('url', 'base'))


@book_blueprint.route('/', methods=['GET'])
def render_all_books():
    """Render all books."""
    books = db.session.query(models.Book)
    print(books)
    return render_template('books.html',
                           books=books)


@book_blueprint.route('/<int:book_id>', methods=['GET'])
def render_book_by_id(book_id):
    """Render book by idea."""
    book = db.session.query(models.Book).get(book_id)
    return render_template('book.html',
                           book=book)
