"""Handle all searches."""

from sqlalchemy import text
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
        results = {g.id: g.text_ for g in glosses}
    else:
        sql = 'SELECT * FROM gloss WHERE MATCH (text_) AGAINST (:keyword)'
        conn = db.engine.connect()
        try:
            t = conn.execute(text(sql), keyword=keyword)
            results = {r[0]: r[3] for r in t}
        except:
            results = []
        finally:
            conn.close()
    return jsonify({
        'results': results
    })
