"""Handle all searches."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify

from glossary.config import config
from glossary import db, models


search_blueprint = Blueprint('search',
                             __name__,
                             url_prefix='%s/search' % config.get('url', 'base'))


@search_blueprint.route('/', methods=['GET'], defaults={'keyword': None})
@search_blueprint.route('/<string:keyword>', methods=['GET'])
def search_based_on_keyword(keyword):
    """Search all glosses based on keyword."""
    if not keyword:
        glosses = db.session.query(models.Gloss).all()
        results = [{'id': g.id,
                    'type_': g.type_,
                    'text_': g.text_,
                    'has_entity': (g.entity is not None)} for g in glosses]
    else:
        sql = 'SELECT id, type_, text_, entity_fk FROM gloss WHERE MATCH (text_) AGAINST (:keyword)'
        conn = db.engine.connect()
        try:
            t = conn.execute(text(sql), keyword=keyword)
            results = [{'id': g[0],
                        'type_': g[1],
                        'text_': g[2],
                        'has_entity': g[3] is not None} for g in t]
        except SQLAlchemyError:
            results = []
        finally:
            conn.close()
    return jsonify({
        'results': results
    })
