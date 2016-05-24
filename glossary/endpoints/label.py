"""Render label-related pages."""

from flask import Blueprint, render_template

from glossary import db, models
from glossary.config import config


label_blueprint = Blueprint('label',
                            __name__,
                            url_prefix='%s/label' % config.get('url', 'base'))


@label_blueprint.route('/', methods=['GET'])
def render_labels():
    labels = db.session.query(models.Label).all()
    return render_template('label/labels.html',
                           labels=labels)


@label_blueprint.route('/<string:label_name>', methods=['GET'])
def render_all_with_label(label_name):
    """Render all entities and glosses with label."""

    # if label_name == 'blog':
    #      return render_blog()

    label_name = label_name.lower()
    books = db.session.query(models.Book)\
        .join(models.Label, models.Book.labels)\
        .filter(models.Label.name == label_name)\
        .all()
    ideas = db.session.query(models.Idea)\
        .join(models.Label, models.Idea.labels)\
        .filter(models.Label.name == label_name)\
        .all()
    papers = db.session.query(models.Paper)\
        .join(models.Label, models.Paper.labels)\
        .filter(models.Label.name == label_name)\
        .all()
    talks = db.session.query(models.Talk)\
        .join(models.Label, models.Talk.labels)\
        .filter(models.Label.name == label_name)\
        .all()
    return render_template('label/label.html', label_name=label_name, books=books,
                           ideas=ideas, papers=papers, talks=talks)


@label_blueprint.route('/delete/<int:label_id>/<string:type_>/<int:type_id>', methods=['GET'])
def delete_label_on_entity_or_gloss(label_id, type_, type_id):
    """."""
    if type_ == 'gloss':
        model = models.Gloss
    else:
        model = models.type_to_class[type_]
    instance = db.session.query(model).get(type_id)
    labels = db.session.query(models.Label).all()
    return render_template('label/labels.html',
                           labels=labels)


# def render_blog():
#     """Renders glosses for blog."""
#     entries = db.session.query(models.Gloss)\
#         .join(models.Label, models.Gloss.labels)\
#         .filter(models.Label.name == 'blog')\
#         .all()
#     return render_template('blog.html', entries=entries)
