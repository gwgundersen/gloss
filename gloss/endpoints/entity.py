"""Render individual entity-related pages."""

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required

from gloss import db, models
from gloss.config import config
from gloss.dbutils import get_or_create


entity_blueprint = Blueprint('entity',
                             __name__,
                             url_prefix='%s/entity' % config.get('url', 'base'))


@entity_blueprint.route('/', methods=['GET'])
@login_required
def render_entity_options():
    return render_template('entity/list.html')


@entity_blueprint.route('/<string:type_>', methods=['GET'])
@login_required
def render_entities(type_):
    """Render entity by ID."""
    Class_ = models.type_to_class[type_]
    order_fn = models.type_to_order[type_]
    entities = db.session.query(Class_).order_by(order_fn.desc()).all()
    return render_template('entity/entities.html',
                           type_=type_,
                           entities=entities,
                           stats=Class_.stats())


@entity_blueprint.route('/<int:entity_id>', methods=['GET'])
@login_required
def render_entity_by_just_id(entity_id):
    """Render entity by ID."""
    entity = db.session.query(models.Entity).get(entity_id)
    if not entity:
        return redirect('404.html')
    return render_template('index.html', glosses=entity.glosses, entity=entity)


@entity_blueprint.route('/create', defaults={'type_': None}, methods=['GET'])
@entity_blueprint.route('/<string:type_>/create', methods=['GET'])
@login_required
def render_add_specific_entity_page(type_):
    """Render page for adding a specific entity, e.g. Paper versus Book."""
    if not type_:
        return render_template('entity/create_menu.html')
    return render_template('entity/create_%s.html' % type_)


@entity_blueprint.route('/create/<string:type_>', methods=['POST'])
@login_required
def create_entity(type_):
    """Add entity to database."""
    model = models.type_to_class[type_]
    args = _process_arguments(**request.form)
    instance = model(**args)
    is_book = type_ == 'book'
    instance = _get_or_create_authors(instance, is_book)
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


def _get_or_create_authors(instance, is_book):
    """Get or create authors and attach to instance if necesary."""
    author_names = request.form.get('authors')
    if author_names and author_names != '':
        authors = []
        if ',' in author_names:
            parts = author_names.split(',')
        else:
            parts = author_names.split(';')
        for name in parts:
            name = name.strip()
            author = get_or_create(models.Author, name=name)
            if is_book:
                author.is_female   = request.form.get('is_female')
                author.is_poc      = request.form.get('is_poc')
                author.nationality = request.form.get('nationality')
            db.session.merge(author)
            authors.append(author)
        instance.authors = authors
    return instance


def _get_or_create_journal(instance):
    """Create journal and attach to instance if necessary."""
    if 'journal' in request.form:
        name = request.form.get('journal')
        name = name.strip()
        journal = get_or_create(models.Journal, name=name)
        instance.journal = journal
    return instance


def _process_arguments(**kwargs):
    """Process arguments in preparation to be used to create model."""
    # Remove attributes that will be created as separate objects and added
    # via the ORM.
    for key in ['authors', 'journal', 'is_female', 'is_poc', 'nationality']:
        if key in kwargs:
            del kwargs[key]
    # Convert plain text to keywords.
    for a in kwargs:
        v = kwargs[a]
        # Not sure why, but the form sends the attributes as lists.
        if type(v) == list:
            kwargs[a] = v[0]
        v = kwargs[a]
        if v == 'true' or v == 'True' or v == 1:
            kwargs[a] = True
        if v == 'false' or v == 'False' or v == 0:
            kwargs[a] = False
        if v == '' or v == 'null':
            kwargs[a] = None
    return kwargs
