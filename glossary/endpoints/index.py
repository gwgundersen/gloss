"""Render landing page."""

from flask import Blueprint, render_template

from glossary import db, models
from glossary.config import config


index_blueprint = Blueprint('index',
                            __name__,
                            url_prefix=config.get('url', 'base'))


@index_blueprint.route('/', methods=['GET'])
def render_index_page():
    """Render index page."""
    glosses = db.session.query(models.Gloss)
    return render_template('index.html',
                           glosses=glosses)
