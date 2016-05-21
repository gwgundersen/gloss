"""Define all primary objects in program."""

from entity import Entity
from label import Label

# Glosses
from gloss import Gloss
from summary import Summary
from thought import Thought

# Entities
from idea import Idea
from paper import Paper
from book import Book
from talk import Talk

# Misc
from author import Author
from journal import Journal

# Joins
from author_to_book import author_to_book
from author_to_paper import author_to_paper
from author_to_talk import author_to_talk

from label_to_book import label_to_book
from label_to_idea import label_to_idea
from label_to_paper import label_to_paper
from label_to_talk import label_to_talk

type_to_class = {
    'book': Book,
    'idea': Idea,
    'paper': Paper,
    'talk': Talk
}
