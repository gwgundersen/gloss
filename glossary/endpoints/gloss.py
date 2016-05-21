"""Render gloss pages."""

from datetime import datetime
from flask import Blueprint, redirect, request, render_template, url_for
import pypandoc

from glossary import db, models
from glossary.config import config


gloss_blueprint = Blueprint('gloss',
                            __name__,
                            url_prefix='%s/gloss' % config.get('url', 'base'))


@gloss_blueprint.route('/', methods=['GET'])
def render_all_glosses():
    """Render all glosses."""
    glosses = db.session.query(models.Gloss).all()
    return render_template('gloss/glosses.html',
                           glosses=glosses)


@gloss_blueprint.route('/<int:gloss_id>', methods=['GET'])
def render_gloss(gloss_id):
    """Render gloss by ID."""
    gloss = db.session.query(models.Gloss).get(gloss_id)
    pdoc_args = ['--mathjax',]
    output = pypandoc.convert(gloss.text_,
                              to='html5',
                              format='md',
                              extra_args=pdoc_args)
    return render_template('gloss/gloss.html', gloss_id=gloss_id,
                           entity=gloss.entity,
                           rendered_gloss=output)


@gloss_blueprint.route('/<string:gloss_type>', methods=['GET'])
def render_gloss_type(gloss_type):
    """Render all glosses of a type."""
    glosses = db.session.query(models.Gloss).filter_by(type_=gloss_type).all()
    return render_template('gloss/glosses.html', glosses=glosses)


@gloss_blueprint.route('/add', defaults={'entity_id': None}, methods=['GET'])
@gloss_blueprint.route('/add/<int:entity_id>', methods=['GET'])
def render_add_gloss_page(entity_id):
    """Render page to add gloss."""
    if entity_id:
        entity = db.session.query(models.Entity).get(entity_id)
        return render_template('gloss/add_to_specific_entity.html',
                               entity=entity)
    entities = db.session.query(models.Entity).all()
    for e in entities:
        print(e.title)
    return render_template('gloss/add.html',
                           entities=entities)


@gloss_blueprint.route('/add', methods=['POST'])
def add_gloss():
    """Add new gloss."""
    entity_id = int(request.form.get('entity_id'))
    text_ = request.form.get('text_', '')
    type_ = request.form.get('type_', 'thought')
    entity = db.session.query(models.Entity).get(entity_id)
    now = datetime.now()
    gloss = models.Gloss(text_=text_, type_=type_, timestamp=now)
    entity.glosses.append(gloss)
    db.session.merge(entity)
    db.session.commit()
    return redirect(url_for('entity.render_entity_by_id',
                            type_=entity.type_,
                            entity_id=entity.id))


@gloss_blueprint.route('/delete/<int:gloss_id>', methods=['POST'])
def delete_gloss(gloss_id):
    """Delete gloss by ID."""
    gloss = db.session.query(models.Gloss).get(gloss_id)
    db.session.delete(gloss)
    db.session.commit()
    return redirect(url_for('gloss.render_all_glosses'))


@gloss_blueprint.route('/edit/<int:gloss_id>', methods=['GET', 'POST'])
def edit_gloss(gloss_id):
    """Edit gloss."""
    gloss = db.session.query(models.Gloss).get(gloss_id)
    if request.method == 'GET':
        return render_template('gloss/edit.html', gloss=gloss)
    else:
        gloss.text_= request.form.get('text_')
        db.session.merge(gloss)
        db.session.commit()
        return redirect(url_for('gloss.render_gloss', gloss_id=gloss_id))
