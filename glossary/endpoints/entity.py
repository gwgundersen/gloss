"""Render individual entity-related pages."""

from flask import Blueprint, request, render_template, redirect, url_for

from glossary import db, models
from glossary.config import config


entity_blueprint = Blueprint('entity',
                             __name__,
                             url_prefix='%s/entity' % config.get('url', 'base'))


type_to_class = {
    'book': models.Book,
    'idea': models.Idea,
    'paper': models.Paper,
    'talk': models.Talk
}


@entity_blueprint.route('/', methods=['GET'])
def render_entity_types():
    """Render entity types."""
    return render_template('entity/entity_types.html')


@entity_blueprint.route('/<string:type_>', methods=['GET'])
def render_entities(type_):
    """Render entity by ID."""
    Class_ = type_to_class[type_]
    entities = db.session.query(Class_).all()
    return render_template('entity/entities.html',
                           type_=type_,
                           entities=entities)


@entity_blueprint.route('/<string:type_>/<int:entity_id>', methods=['GET'])
def render_entity_by_id(type_, entity_id):
    """Render entity by ID."""
    Class_ = type_to_class[type_]
    entity = db.session.query(Class_).get(entity_id)
    if not entity:
        return redirect('404.html')
    return render_template('entity/entity.html',
                           entity=entity)


@entity_blueprint.route('/add', methods=['GET'])
def render_add_entity_page():
    """Render page with list of available entities."""
    return render_template('entity/add_entity_types.html')


@entity_blueprint.route('/<string:type_>/add', methods=['GET'])
def render_add_specific_entity_page(type_):
    """Render page for adding a specific entity, e.g. Idea versus Book."""
    Class_ = type_to_class[type_]
    attrs = []
    for c in Class_.__table__.columns:
        if c.name == 'id' or c.name.endswith('_fk'):
            continue
        attrs.append({
            'name': c.name,
            'type_': c.type
        })
    return render_template('entity/add.html',
                           type_=type_,
                           attrs=attrs)


@entity_blueprint.route('/<string:type_>/add', methods=['POST'])
def add_entity(type_):
    """Add entity to database."""
    model = type_to_class[type_]
    args = _process_arguments(**request.form)
    instance = model(**args)
    instance = _get_or_create_authors(instance)
    instance = _get_or_create_labels(instance)
    instance = _get_or_create_journal(instance)
    db.session.add(instance)
    db.session.commit()
    return redirect(url_for('gloss.render_add_gloss_page',
                            entity_id=instance.id))


def _get_or_create_authors(instance):
    """Get or create authors and attach to instance if necesary."""
    if 'authors' in request.form:
        authors = []
        for a in request.form.get('authors').split(','):
            t = a.strip().split(' ')
            fn = t[0].capitalize()
            ln = t[1].capitalize()
            author = _get_or_create(models.Author, first_name=fn,
                                    last_name=ln)
            authors.append(author)
        instance.authors = authors
    return instance


def _get_or_create_labels(instance):
    """Get or create labels and attach to instance if necessary."""
    if 'labels' in request.form:
        labels = []
        for l in request.form.get('labels').split(','):
            label = _get_or_create(models.Label, name=l.strip())
            labels.append(label)
        instance.labels = labels
    return instance


def _get_or_create_journal(instance):
    """Create journal and attach to instance if necessary."""
    if 'journal' in request.form:
        j = request.form.get('journal')
        j = j.strip().capitalize()
        journal = _get_or_create(models.Journal, name=j)
        instance.journal = journal
    return instance


def _get_or_create(model, **kwargs):
    """Return instance if it exists, create it otherwise."""
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance


def _process_arguments(**kwargs):
    """Process arguments in preparation to be used to create model."""
    # Remove attributes that will be created as separate objects and added
    # via the ORM.
    if 'authors' in kwargs:
        del kwargs['authors']
    if 'labels' in kwargs:
        del kwargs['labels']
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
        if v == 'null':
            kwargs[a] = None
    return kwargs
