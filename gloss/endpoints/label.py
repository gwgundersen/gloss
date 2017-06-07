"""Render label-related pages."""

from flask import Blueprint, jsonify, redirect, request
from flask.ext.login import login_required

from gloss import db, models
from gloss.config import config
from gloss import dbutils


label_blueprint = Blueprint('label',
                            __name__,
                            url_prefix='%s/label' % config.get('url', 'base'))


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
