"""Render gloss pages."""

from flask import Blueprint, render_template
import pypandoc

from glossary import db, models
from glossary.config import config


gloss_blueprint = Blueprint('gloss',
                            __name__,
                            url_prefix='%s/gloss' % config.get('url', 'base'))


@gloss_blueprint.route('/<int:gloss_id>', methods=['GET'])
def render_gloss(gloss_id):
    """Render glossary."""
    gloss = db.session.query(models.Gloss).get(gloss_id)
    pdoc_args = ['--mathjax', '--smart']
    output = pypandoc.convert(gloss.text_,
                              to='html5',
                              format='md',
                              extra_args=pdoc_args)
    return render_template('gloss.html',
                           rendered_gloss=output)