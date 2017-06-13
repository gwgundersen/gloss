"""Custom filters for Jinja2 templates."""

from flask import Blueprint
import jinja2
from gloss import renderengine


jinjafilters = Blueprint('filters', __name__)


@jinja2.contextfilter
@jinjafilters.app_template_filter('markdown')
def to_markdown(context, value):
    return renderengine.render_markdown(value)


@jinja2.contextfilter
@jinjafilters.app_template_filter('preview')
def to_markdown(context, value):
    return value[:200] + '...'


@jinja2.contextfilter
@jinjafilters.app_template_filter('date_str')
def to_date_str(context, value):
    if not value:
        return ''
    return value.strftime('%Y-%m-%d')


@jinja2.contextfilter
@jinjafilters.app_template_filter('datetime_str')
def to_datetime_str(context, value):
    if not value:
        return ''
    return value.strftime('%d %b %Y, %a, %H:%M')
