"""Render landing page."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify, render_template, request

from glossary import db, models
from glossary.config import config


index_blueprint = Blueprint('index',
                            __name__,
                            url_prefix=config.get('url', 'base'))



@index_blueprint.route('/', methods=['GET'], defaults={'keyword': None})
@index_blueprint.route('/<string:keyword>', methods=['GET'])
def render_index_page(keyword):
    """Render index page."""
    labels = db.session.query(models.Label).all()
    if not keyword:
        glosses = db.session.query(models.Gloss)\
            .filter_by(archive=False)\
            .order_by(models.Gloss.timestamp.desc())
        return render_template('index.html', glosses=glosses,
                               is_glossary=True, labels=labels)
    else:
        results = _get_glosses_by_keyword(keyword)
        #results += _get_entity_by_keyword('idea', keyword)
        #results += _get_entity_by_keyword('paper', keyword)
        #results += _get_entity_by_keyword('book', keyword)
        #results += _get_entity_by_keyword('talk', keyword)
        return render_template('index.html', glosses=results,
                               is_glossary=True, labels=labels)


@index_blueprint.route('/archive', methods=['POST'])
def archive_glosses():
    gloss_ids = request.form.getlist('gloss_ids[]')
    for id_ in gloss_ids:
        id_ = int(id_)
        gloss = db.session.query(models.Gloss).get(id_)
        gloss.archive = True
        db.session.merge(gloss)
        db.session.commit()
    return jsonify({
        'status': 'success'
    })


@index_blueprint.route('/label', methods=['POST'])
def label_glosses():
    gloss_ids = request.form.getlist('gloss_ids[]')
    label_id = request.form.get('label_id')
    label = db.session.query(models.Label).get(label_id)
    for id_ in gloss_ids:
        id_ = int(id_)
        gloss = db.session.query(models.Gloss).get(id_)
        gloss.labels.append(label)
        db.session.merge(gloss)
        db.session.commit()
    return jsonify({
        'status': 'success'
    })



def _get_glosses_by_keyword(keyword):
    """Return glosses based on keyword matches in text."""
    sql = 'SELECT id FROM gloss WHERE MATCH (text_) AGAINST (:keyword)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids = [int(g[0]) for g in t]
    glosses = db.session.query(models.Gloss)\
        .filter(models.Gloss.id.in_(ids)).all()
    return glosses


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