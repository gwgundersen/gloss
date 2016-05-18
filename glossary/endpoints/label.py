"""Render label-related pages."""

from flask import Blueprint, render_template

from glossary import db, models
from glossary.config import config


label_blueprint = Blueprint('label',
                            __name__,
                            url_prefix='%s/label' % config.get('url', 'base'))


@label_blueprint.route('/<string:label_name>', methods=['GET'])
def render_all_with_label(label_name):
    """Render all entities and glosses with label."""
    label_name = label_name.lower()
    papers = db.session.query(models.Paper)\
        .join(models.Label, models.Paper.labels)\
        .filter(models.Label.name == label_name)\
        .all()
    books = db.session.query(models.Book)\
        .join(models.Label, models.Book.labels)\
        .filter(models.Label.name == label_name)\
        .all()
    return render_template('label.html',
                           label_name=label_name,
                           books=books,
                           papers=papers)
