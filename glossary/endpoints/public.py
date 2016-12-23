"""Render public glosses."""

from flask import Blueprint, render_template

from glossary import db, config, models


url_prefix = '%s/%s' % (config.get('url', 'base'), config.get('url', 'public'))
public_blueprint = Blueprint('public',
                             __name__,
                             url_prefix=url_prefix)


@public_blueprint.route('/<int:gloss_id>/<string:title>', methods=['GET'])
def render_public_gloss(gloss_id, title):
    """Render gloss by ID. We don't care about the title. It is just sugar,
    similar to StackOverflow's URLs."""
    gloss = db.session.query(models.Gloss).get(gloss_id)
    if not gloss.is_public:
        return 'Nothin to see here folks.'
    labels = db.session.query(models.Label)\
        .order_by(models.Label.name.asc()).all()
    return render_template('gloss/public.html', gloss=gloss, labels=labels)
