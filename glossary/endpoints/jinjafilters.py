"""Custom filters for Jinja2 templates."""

from flask import Blueprint
import jinja2
import pypandoc


jinjafilters = Blueprint('filters', __name__)


# Data filters
# ----------------------------------------------------------------------------
@jinja2.contextfilter
@jinjafilters.app_template_filter('markdown')
def to_markdown(context, value):
    return pypandoc.convert(value,
                            to='html5',
                            format='md',
                            extra_args=['--mathjax'])
