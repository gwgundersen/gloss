"""Render blog-related pages."""

from flask import Blueprint, render_template

from glossary import db, config, models


blog_blueprint = Blueprint('blog',
                           __name__,
                           url_prefix='%s/blog' % config.get('url', 'base'))


@blog_blueprint.route('/', methods=['GET'])
def render_blog():
    """Render blog. Careful, even if a gloss is private."""
    # .filter(models.Gloss.is_private == False)\
    glosses = db.session.query(models.Gloss)\
        .join(models.Label, models.Gloss.labels)\
        .filter(models.Label.name == 'blog')\
        .order_by(models.Gloss.timestamp.desc())\
        .all()
    return render_template('blog.html', glosses=glosses)
