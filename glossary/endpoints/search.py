"""Handle all searches."""

from sqlalchemy import text
from flask import Blueprint, jsonify

from glossary.config import config
from glossary import db


search_blueprint = Blueprint('search',
                             __name__,
                             url_prefix='%s/search' % config.get('url', 'base'))


@search_blueprint.route('/<string:keyword>', methods=['GET'])
def search_based_on_keyword(keyword):
    """Search all glosses based on keyword."""
    sql = text('SELECT * FROM gloss WHERE MATCH (text_) AGAINST (:keyword)')
    conn = db.engine.connect()
    results = []
    try:
        t = conn.execute(sql, keyword=keyword)
        results = {r[0]: r[3] for r in t}
    finally:
        conn.close()
    return jsonify({
        'results': results
    })
