"""Render landing page."""

from flask import Blueprint, jsonify, render_template, request

from glossary import db, models
from glossary.config import config


index_blueprint = Blueprint('index',
                            __name__,
                            url_prefix=config.get('url', 'base'))


@index_blueprint.route('/', methods=['GET'])
def render_index_page():
    """Render index page."""
    glosses = db.session.query(models.Gloss)\
        .filter_by(archive=False)\
        .order_by(models.Gloss.timestamp.desc())
    labels = db.session.query(models.Label).all()
    return render_template('index.html', glosses=glosses, is_glossary=True,
                           labels=labels)


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
