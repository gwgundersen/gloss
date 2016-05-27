"""Render individual entity-related pages."""

from flask import Blueprint, request, render_template, redirect, url_for
from flask.ext.login import current_user, login_required

from glossary import db, models
from glossary.config import config
from glossary.dbutils import get_or_create


entity_blueprint = Blueprint('entity',
                             __name__,
                             url_prefix='%s/entity' % config.get('url', 'base'))


@entity_blueprint.route('/<string:type_>', methods=['GET'])
def render_entities(type_):
    """Render entity by ID."""
    # TODO: Manually checking the type_ here is poor design!
    auth = current_user.is_authenticated
    if not auth and type_ == 'idea':
        return redirect(url_for('index.render_index_page'))
    Class_ = models.type_to_class[type_]
    order_fn = models.type_to_order[type_]
    entities = db.session.query(Class_).order_by(order_fn.desc()).all()
    return render_template('entity/entities.html',
                           type_=type_,
                           entities=entities,
                           stats=Class_.stats(),
                           is_private=auth)


@entity_blueprint.route('/<int:entity_id>', methods=['GET'])
def render_entity_by_just_id(entity_id):
    """Render entity by ID."""
    entity = db.session.query(models.Entity).get(entity_id)
    if not entity:
        return redirect('404.html')
    return render_template('entity/entity.html',
                           entity=entity,
                           is_private=current_user.is_authenticated)


@entity_blueprint.route('/<string:type_>/<int:entity_id>', methods=['GET'])
def render_entity_by_id(type_, entity_id):
    """Render entity by ID."""
    Class_ = models.type_to_class[type_]
    entity = db.session.query(Class_).get(entity_id)
    if not entity:
        return redirect('404.html')
    return render_template('entity/entity.html',
                           entity=entity)


@entity_blueprint.route('/create', defaults={'type_': None}, methods=['GET'])
@entity_blueprint.route('/<string:type_>/create', methods=['GET'])
@login_required
def render_add_specific_entity_page(type_):
    """Render page for adding a specific entity, e.g. Idea versus Book."""
    if not type_:
        return render_template('entity/create_menu.html')
    Class_ = models.type_to_class[type_]
    attrs = []
    for c in Class_.__table__.columns:
        if c.name == 'id' or c.name.endswith('_fk'):
            continue
        attrs.append({
            'name': c.name,
            'type_': c.type
        })
    return render_template('entity/create.html',
                           type_=type_,
                           attrs=attrs)


@entity_blueprint.route('/create/<string:type_>', methods=['POST'])
@login_required
def create_entity(type_):
    """Add entity to database."""
    model = models.type_to_class[type_]
    args = _process_arguments(**request.form)
    instance = model(**args)
    instance = _get_or_create_authors(instance)
    instance = _get_or_create_journal(instance)
    db.session.add(instance)
    db.session.commit()
    return redirect(url_for('gloss.render_add_gloss_page',
                            entity_id=instance.id))


@entity_blueprint.route('/delete/<entity_id>', methods=['POST'])
@login_required
def delete_entity(entity_id):
    """Deletes entity from database."""
    entity = db.session.query(models.Entity).get(entity_id)
    db.session.delete(entity)
    db.session.commit()
    return redirect(url_for('index.render_index_page'))


def _get_or_create_authors(instance):
    """Get or create authors and attach to instance if necesary."""
    if 'authors' in request.form:
        authors = []
        for a in request.form.get('authors').split(';'):
            parts = a.split(',')
            name = parts[0].strip().split(' ')
            fn = name[0].capitalize()
            ln = name[1].capitalize()
            if len(parts) > 1:
                is_female = parts[1].strip() == 'female'
                is_poc = parts[2].strip() == 'poc'
            else:
                is_female = None
                is_poc = None
            author = get_or_create(models.Author, first_name=fn,
                                   last_name=ln, is_female=is_female,
                                   is_poc=is_poc)
            authors.append(author)
        instance.authors = authors
    return instance


def _get_or_create_journal(instance):
    """Create journal and attach to instance if necessary."""
    if 'journal' in request.form:
        j = request.form.get('journal')
        j = j.strip().capitalize()
        journal = get_or_create(models.Journal, name=j)
        instance.journal = journal
    return instance


def _process_arguments(**kwargs):
    """Process arguments in preparation to be used to create model."""
    # Remove attributes that will be created as separate objects and added
    # via the ORM.
    if 'authors' in kwargs:
        del kwargs['authors']
    if 'journal' in kwargs:
        del kwargs['journal']
    # Convert plain text to keywords.
    for a in kwargs:
        v = kwargs[a]
        # Not sure why, but the form sends the attributes as lists.
        if type(v) == list:
            kwargs[a] = v[0]
        v = kwargs[a]
        if v == 'true':
            kwargs[a] = True
        if v == 'false':
            kwargs[a] = False
        if v == '' or v == 'null':
            kwargs[a] = None
    return kwargs
