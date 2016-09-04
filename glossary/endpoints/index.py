"""Render landing page."""

from sqlalchemy import text
from flask import Blueprint, render_template, request
from flask.ext.login import login_required

from glossary import db, models
from glossary.config import config


index_blueprint = Blueprint('index',
                            __name__,
                            url_prefix=config.get('url', 'base'))


@index_blueprint.route('/', methods=['GET'])
@login_required
def render_index_page():
    """Render index page."""
    keyword = request.args.get('q')
    labels = db.session.query(models.Label).all()
    if not keyword:
        glosses = db.session.query(models.Gloss)\
            .filter((models.Gloss.archive == False) |
                    (models.Gloss.type_ == 'todo'))\
            .order_by(models.Gloss.timestamp.desc())
        return render_template('index.html', glosses=glosses,
                               show_nav_controls=True, labels=labels)
    else:
        results = _get_glosses_by_keyword(keyword)
        return render_template('index.html', glosses=results,
                               show_nav_controls=True, labels=labels)


def _get_glosses_by_keyword(keyword):
    """Return glosses based on keyword matches in text."""
    sql = 'SELECT id FROM gloss WHERE MATCH (text_) AGAINST (:keyword)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids = [int(g[0]) for g in t]
    glosses = db.session.query(models.Gloss)\
        .filter(models.Gloss.id.in_(ids)).all()
    return glosses
