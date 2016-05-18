"""Render individual entity-related pages."""

from flask import Blueprint, render_template

from glossary import db, models
from glossary.config import config


entity_blueprint = Blueprint('entity',
                            __name__,
                            url_prefix='%s/entity' % config.get('url', 'base'))


type_to_class = {
    'book': models.Book,
    'paper': models.Paper
}


@entity_blueprint.route('/<string:type_>', methods=['GET'])
def render_entities(type_):
    """Render entity by ID."""
    model = type_to_class[type_]
    entities = db.session.query(model).all()
    print(entities)
    print(type_)
    return render_template('entities.html',
                           type_=type_,
                           entities=entities)


@entity_blueprint.route('/<string:type_>/<int:entity_id>', methods=['GET'])
def render_entity_by_id(type_, entity_id):
    """Render entity by ID."""
    model = type_to_class[type_]
    entity = db.session.query(model).get(entity_id)
    return render_template('entity.html',
                           entity=entity)
