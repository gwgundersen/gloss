"""Define all primary objects in program."""

from entity import Entity
from label import Label

# Glosses
from glossary.models.gloss import Gloss

# Entities
from idea import Idea
from paper import Paper
from book import Book
from talk import Talk

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
    'idea': Idea,
    'paper': Paper,
    'talk': Talk
}

type_to_order = {
    'book': Book.ended,
    'idea': Idea.title,
    'paper': Paper.date_read,
    'talk': Talk.timestamp
}
