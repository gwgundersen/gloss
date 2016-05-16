"""Render paper-related pages."""

from flask import Blueprint, render_template

from glossary import db, models
from glossary.config import config


paper_blueprint = Blueprint('paper',
                            __name__,
                            url_prefix='%s/paper' % config.get('url', 'base'))


@paper_blueprint.route('/', methods=['GET'])
def render_all_papers():
    """Render all papers."""
    papers = db.session.query(models.Paper)
    return render_template('papers.html',
                           papers=papers)
