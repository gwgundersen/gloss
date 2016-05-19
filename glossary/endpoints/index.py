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
    papers = db.session.query(models.Paper)
    print(papers[0].title)
    return render_template('index.html',
                           papers=papers)
