"""Render landing page."""

from sqlalchemy import text
from flask import Blueprint, render_template, request
from flask.ext.login import login_required

from gloss import db, models
from gloss.config import config


index_blueprint = Blueprint('index',
                            __name__,
                            url_prefix=config.get('url', 'base'))


@index_blueprint.route('/', methods=['GET'])
@login_required
def render_index_page():
    """Render index page."""
    keyword = request.args.get('q')
    labels = db.session.query(models.Label)\
        .order_by(models.Label.name)\
        .all()
    if not keyword:
        glosses = db.session.query(models.Gloss)\
            .filter((models.Gloss.archive == False))\
            .order_by(models.Gloss.timestamp.desc())
    elif keyword == 'all':
        glosses = db.session.query(models.Gloss).all()
    # E.g. the label search for "ai": "?q=label.ai".
    elif keyword.startswith('label.'):
        label_name = keyword.split('.')[1]
        glosses = db.session.query(models.Gloss)\
            .join(models.Label, models.Gloss.labels)\
            .filter(models.Label.name == label_name)\
            .all()
        labels = db.session.query(models.Label).all()
    else:
        glosses = _get_glosses_by_keyword(keyword)
    return render_template('index.html', glosses=glosses, labels=labels)


def _get_glosses_by_keyword(keyword):
    """Return glosses based on keyword matches in text."""
    sql = 'SELECT id FROM gloss WHERE MATCH (text_) AGAINST (:keyword)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids = [int(g[0]) for g in t]
    glosses = db.session.query(models.Gloss)\
        .filter(models.Gloss.id.in_(ids)).all()
    return glosses
