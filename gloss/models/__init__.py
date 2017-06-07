"""Define all primary objects in program."""

from label import Label

# Glosses
from gloss.models.gloss_ import Gloss

# Entities
from gloss.models.entity.entity import Entity
from gloss.models.entity.book import Book
from gloss.models.entity.paper import Paper
from gloss.models.entity.talk import Talk
from gloss.models.entity.website import Website

# Misc
from author import Author
from journal import Journal
from user import User

# Joins
from author_to_book import author_to_book
from author_to_paper import author_to_paper
from author_to_talk import author_to_talk

from label_to_gloss import label_to_gloss

type_to_class = {
    'book': Book,
    'paper': Paper,
    'talk': Talk,
    'website': Website
}

type_to_order = {
    'book': Book.ended,
    'paper': Paper.date_read,
    'talk': Talk.timestamp,
    'website': Website.title
}
