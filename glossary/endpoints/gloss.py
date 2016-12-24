"""Render gloss pages."""

from datetime import datetime
from flask import Blueprint, jsonify, redirect, request, render_template, \
    url_for
from flask.ext.login import login_required

from glossary import db, models
from glossary.config import config
from glossary import dbutils, render


gloss_blueprint = Blueprint('gloss',
                            __name__,
                            url_prefix='%s/gloss' % config.get('url', 'base'))


@gloss_blueprint.route('/<int:gloss_id>', methods=['GET'])
@login_required
def render_gloss(gloss_id):
    """Render gloss by ID."""
    gloss = db.session.query(models.Gloss).get(gloss_id)
    return render_template('gloss/gloss.html', gloss=gloss)


@gloss_blueprint.route('/preview', methods=['POST'])
@login_required
def preview_gloss():
    """Preview gloss by ID for editing UI."""
    text = request.form.get('text')
    return render.render_markdown(text)


@gloss_blueprint.route('/create', defaults={'entity_id': None}, methods=['GET'])
@gloss_blueprint.route('/create/<int:entity_id>', methods=['GET'])
@login_required
def render_add_gloss_page(entity_id):
    """Render page to add gloss."""
    if entity_id:
        entity = db.session.query(models.Entity).get(entity_id)
        return render_template('gloss/add_to_specific_entity.html',
                               entity=entity)
    entities = db.session.query(models.Entity).all()
    return render_template('gloss/create.html',
                           entities=entities)


@gloss_blueprint.route('/create', methods=['POST'])
@login_required
def create_gloss():
    """Create new gloss."""
    entity_id = request.form.get('entity_id')
    text_ = request.form.get('text_') or ''
    now = datetime.now()
    gloss = models.Gloss(text_=text_, timestamp=now)
    dbutils.get_or_create_labels(request, gloss)
    if entity_id:
        entity = db.session.query(models.Entity).get(entity_id)
        entity.glosses.append(gloss)
        db.session.merge(entity)
    else:
        db.session.add(gloss)
    db.session.commit()
    return redirect(url_for('gloss.render_gloss', gloss_id=gloss.id))


@gloss_blueprint.route('/delete/<int:gloss_id>', methods=['POST'])
@login_required
def delete_gloss(gloss_id):
    """Delete gloss by ID."""
    gloss = db.session.query(models.Gloss).get(gloss_id)
    db.session.delete(gloss)
    db.session.commit()
    return redirect(url_for('index.render_index_page'))


@gloss_blueprint.route('/edit/<int:gloss_id>', methods=['GET', 'POST'])
@login_required
def edit_gloss(gloss_id):
    """Edit gloss."""
    gloss = db.session.query(models.Gloss).get(gloss_id)
    if request.method == 'GET':
        labels = db.session.query(models.Label)\
            .order_by(models.Label.name.asc()).all()
        return render_template('gloss/edit.html', gloss=gloss, labels=labels)
    else:
        gloss.text_= request.form.get('text_')
        gloss.timestamp = datetime.now()
        db.session.merge(gloss)
        db.session.commit()
        return redirect(url_for('gloss.render_gloss', gloss_id=gloss_id))


@gloss_blueprint.route('/archive', methods=['POST'])
@login_required
def archive_glosses():
    """Archive gloss."""
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
