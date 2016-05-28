"""Utility methods for managing the database."""

from glossary import db, models


def get_or_create(model, **kwargs):
    """Return instance if it exists, create it otherwise."""
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance


def get_or_create_labels(request, gloss=None):
    """Get or create labels and attach to instance if necessary."""
    label_names = request.form.get('labels')
    if label_names == '':
        return
    labels = []
    for l in label_names.split(','):
        label = get_or_create(models.Label, name=l.strip())
        labels.append(label)
    if gloss:
        gloss.labels = labels
