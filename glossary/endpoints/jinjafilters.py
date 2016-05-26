"""Custom filters for Jinja2 templates."""

from flask import Blueprint
import jinja2
import pypandoc


jinjafilters = Blueprint('filters', __name__)


@jinja2.contextfilter
@jinjafilters.app_template_filter('markdown')
def to_markdown(context, value):
    # try:
    #     output = pypandoc.convert(value, to='html5', format='md',
    #                               extra_args=['--mathjax'])
    # except:
    #     output = value
    # return output
    return pypandoc.convert(value, to='html5', format='md',
                            extra_args=['--mathjax'])


@jinja2.contextfilter
@jinjafilters.app_template_filter('date_str')
def to_date_str(context, value):
    if not value:
        return ''
    return ' - ' + value.strftime('%Y-%m-%d')


@jinja2.contextfilter
@jinjafilters.app_template_filter('datetime_str')
def to_datetime_str(context, value):
    if not value:
        return ''
    return value.strftime('%d %b %Y, %a, %H:%M')
