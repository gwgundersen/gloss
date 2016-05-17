"""Render author-related pages."""

from flask import Blueprint, render_template

from glossary import db, models
from glossary.config import config


author_blueprint = Blueprint('author',
                             __name__,
                             url_prefix='%s/author' % config.get('url', 'base'))


@author_blueprint.route('/<string:author_name>', methods=['GET'])
def render_all_authors(author_name):
    """Render all authors."""
    parts = author_name.split('_')
    author = db.session.query(models.Author)\
        .filter_by(first_name=parts[0])\
        .filter_by(last_name=parts[1])\
        .one()
    return render_template('author.html',
                           author=author)
