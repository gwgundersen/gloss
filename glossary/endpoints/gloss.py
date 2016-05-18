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
    """Render gloss by ID."""
    gloss = db.session.query(models.Gloss).get(gloss_id)
    pdoc_args = ['--mathjax',]
    output = pypandoc.convert(gloss.text_,
                              to='html5',
                              format='md',
                              extra_args=pdoc_args)
    return render_template('gloss.html',
                           entity=gloss.entity,
                           rendered_gloss=output)


@gloss_blueprint.route('/<string:gloss_type>', methods=['GET'])
def render_gloss_type(gloss_type):
    """Render all glosses of a type."""
    glosses = db.session.query(models.Gloss).filter_by(type_=gloss_type).all()
    return render_template('glosses.html', glosses=glosses)
