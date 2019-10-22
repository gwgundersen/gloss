"""Render author-related pages."""

from flask import Blueprint, render_template
from flask_login import login_required

from gloss import db, models
from gloss.config import config


author_blueprint = Blueprint('author',
                             __name__,
                             url_prefix='%s/author' % config.get('url', 'base'))



@author_blueprint.route('/', methods=['GET'])
@login_required
def render_all_authors():
    """Render all authors."""
    authors = db.session.query(models.Author)\
        .order_by(models.Author.name)\
        .all()
    return render_template('authors.html', authors=authors)


@author_blueprint.route('/<int:author_id>', methods=['GET'])
@login_required
def render_author(author_id):
    """Render author by ID."""
    author = db.session.query(models.Author)\
        .filter_by(id=author_id)\
        .one()
    return render_template('author.html', author=author)
