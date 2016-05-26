"""Render label-related pages."""

from flask import Blueprint, jsonify, redirect, request, render_template, url_for
from flask.ext.login import current_user, login_required

from glossary import db, models
from glossary.config import config
from glossary import dbutils


label_blueprint = Blueprint('label',
                            __name__,
                            url_prefix='%s/label' % config.get('url', 'base'))


@label_blueprint.route('/', methods=['GET'])
@login_required
def render_labels():
    labels = db.session.query(models.Label).all()
    return render_template('label/labels.html',
                           labels=labels)


@label_blueprint.route('/<string:label_name>', methods=['GET'])
@login_required
def render_all_with_label(label_name):
    """Render all entities and glosses with label."""
    if not current_user.is_authenticated:
        return redirect(url_for('index.render_index_page'))

    label_name = label_name.lower()
    glosses = db.session.query(models.Gloss)\
        .join(models.Label, models.Gloss.labels)\
        .filter(models.Label.name == label_name)\
        .all()
    labels = db.session.query(models.Label).all()
    return render_template('index_private.html', glosses=glosses,
                           show_nav_controls=True, labels=labels)


@label_blueprint.route('/delete', methods=['POST'])
@login_required
def delete_label_on_gloss():
    """Deletes a label for a specific gloss."""
    gloss_id = request.form.get('gloss_id')
    label_id = request.form.get('label_id')
    label = db.session.query(models.Label).get(label_id)
    if gloss_id:
        gloss = db.session.query(models.Gloss).get(gloss_id)
        gloss.labels.remove(label)
        db.session.commit()
    else:
        db.session.delete(label)
        db.session.commit()
    return redirect(request.referrer)


@label_blueprint.route('/add', methods=['POST'])
@login_required
def label_glosses():
    """Add label to selected gloss(es) or create new label."""
    gloss_ids = request.form.getlist('gloss_ids[]')
    if len(gloss_ids) == 0:
        gloss_id = request.form.get('gloss_id')
        gloss_ids = [gloss_id] if gloss_id else []
    label_id = request.form.get('label_id')
    label = db.session.query(models.Label).get(label_id)
    for id_ in gloss_ids:
        id_ = int(id_)
        gloss = db.session.query(models.Gloss).get(id_)
        if label in gloss.labels:
            continue
        gloss.labels.append(label)
        db.session.merge(gloss)
        db.session.commit()

    if request.form.get('is_js', None):
        return jsonify({'status': 'success'})
    return redirect(request.referrer)


@label_blueprint.route('/create', methods=['POST'])
@login_required
def create_label():
    """Create new label."""
    dbutils.get_or_create_labels(request)
    return redirect(request.referrer)
