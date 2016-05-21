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
def search_by_keyword(keyword):
    """Search all glosses based on keyword."""
    if not keyword:
        glosses = db.session.query(models.Gloss).all()
        results = [{'id': g.id, 'type_': 'gloss', 'text_': g.text_}
                   for g in glosses]
    else:
        results = _get_glosses_by_keyword(keyword)
        results += _get_entity_by_keyword('idea', keyword)
        results += _get_entity_by_keyword('paper', keyword)
        results += _get_entity_by_keyword('book', keyword)
        results += _get_entity_by_keyword('talk', keyword)
    return jsonify({
        'results': results
    })


def _get_glosses_by_keyword(keyword):
    """Return glosses based on keyword matches in text."""
    sql = 'SELECT id, text_ FROM gloss WHERE MATCH (text_) AGAINST (:keyword)'
    conn = db.engine.connect()
    try:
        t = conn.execute(text(sql), keyword=keyword)
        results = [{'id': g[0], 'text_': g[1], 'type_': 'gloss'} for g in t]
    except SQLAlchemyError:
        results = []
    finally:
        conn.close()
    return results


def _get_entity_by_keyword(type_, keyword):
    """Return entity based on type and keyword."""
    model = models.type_to_class[type_]
    sql = 'SELECT entity_fk, title FROM %s WHERE MATCH (title) AGAINST ' \
          '(:keyword)' % str(model.__table__)
    conn = db.engine.connect()
    try:
        t = conn.execute(text(sql), keyword=keyword)
        results = [{'id': e[0], 'text_': e[1], 'type_': type_} for e in t]
        print('results')
        print(results)
    except SQLAlchemyError as e:
        print(e)
        results = []
    finally:
        conn.close()
    return results