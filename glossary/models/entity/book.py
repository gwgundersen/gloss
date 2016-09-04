"""Represent a scientific publication."""

from datetime import datetime
from sqlalchemy.sql import func

from glossary import db
from glossary.models.author import Author
from glossary.models.entity.entity import Entity


class Book(Entity):

    __tablename__ = 'book'
    entity_fk   = db.Column(db.Integer, db.ForeignKey('entity.id'),
                            primary_key=True)
    title       = db.Column(db.String(255))
    reason      = db.Column(db.String(255))
    finished    = db.Column(db.Boolean)
    pages_read  = db.Column(db.Integer)
    year        = db.Column(db.Integer)
    genre       = db.Column(db.String(255))
    started     = db.Column(db.Date)
    ended       = db.Column(db.Date)
    format      = db.Column(db.String(255))
    source      = db.Column(db.String(255))
    buy         = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'book',
    }

    @property
    def author_info(self):
        a = self.authors[0]
        if len(self.authors) > 1:
            return '%s et al' % a.name
        return a.name

    @classmethod
    def stats(cls):
        """Return statistics on books read."""
        first_book = db.session.query(cls).order_by(Book.started.asc())\
            .all()[0]
        started = datetime.combine(first_book.started, datetime.min.time())
        now = datetime.utcnow()
        days_record = (now - started).days
        books_read = db.session.query(cls).count()

        pages_read = db.session.query(func.max(cls.pages_read)).one()[0]
        pages_per_day = round(float(pages_read) / days_record, 2)
        books_per_month = round(books_read / (days_record / 30.42))

        num_authors = db.session.query(Author)\
            .distinct(Author.id)\
            .join(cls, Author.books)\
            .filter(cls.finished)\
            .count()

        num_poc = db.session.query(Author)\
            .distinct(Author.id)\
            .filter(Author.is_poc)\
            .join(cls, Author.books)\
            .filter(cls.finished)\
            .count()
        pct_poc = round(float(num_poc) / num_authors, 2)

        num_female = db.session.query(Author)\
            .distinct(Author.id)\
            .filter(Author.is_female)\
            .join(cls, Author.books)\
            .filter(cls.finished)\
            .count()
        pct_female = round(float(num_female) / num_authors, 2)

        return [
            {'key': 'Days recorded',    'value': days_record},
            {'key': 'Books read',       'value': books_read},
            {'key': 'Total pages read', 'value': pages_read},
            {'key': 'Pages per day',    'value': pages_per_day},
            {'key': 'Books per month',  'value': books_per_month},
            {'key': '% female',         'value': '%s%%' % pct_female},
            {'key': '% POC',            'value': '%s%%' % pct_poc}
        ]
