"""Define all primary objects in program."""

from gloss.models.label import Label

# Glosses
from gloss.models.gloss_ import Gloss

# Entities
from gloss.models.entity.entity import Entity
from gloss.models.entity.book import Book
from gloss.models.entity.course import Course
from gloss.models.entity.paper import Paper
from gloss.models.entity.talk import Talk
from gloss.models.entity.website import Website

# Misc
from gloss.models.author import Author
from gloss.models.journal import Journal
from gloss.models.user import User
from gloss.models.image import Image

# Joins
from gloss.models.author_to_book import author_to_book
from gloss.models.author_to_course import author_to_course
from gloss.models.author_to_paper import author_to_paper
from gloss.models.author_to_talk import author_to_talk
from gloss.models.author_to_website import author_to_website

from gloss.models.label_to_gloss import label_to_gloss

type_to_class = {
    'book': Book,
    'course': Course,
    'paper': Paper,
    'talk': Talk,
    'website': Website
}

type_to_order = {
    'book': Book.ended,
    'course': Course.year,
    'paper': Paper.date_read,
    'talk': Talk.timestamp,
    'website': Website.title
}
