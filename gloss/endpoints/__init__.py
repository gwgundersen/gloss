"""Render all endpoints for application."""

from gloss.endpoints.index import index_blueprint
from gloss.endpoints.gloss_ import gloss_blueprint
from gloss.endpoints.label import label_blueprint
from gloss.endpoints.author import author_blueprint
from gloss.endpoints.jinjafilters import jinjafilters
from gloss.endpoints.entity import entity_blueprint
from gloss.endpoints.auth import auth_blueprint
from gloss.endpoints.public import public_blueprint
from gloss.endpoints.image import image_blueprint
