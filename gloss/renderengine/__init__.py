"""Functions for rendering Markdown and LaTeX as HTML.
"""

import pypandoc
import re


def render_markdown(value):
    """Render Markdown"""
    try:
        output = pypandoc.convert_text(value, to='html5', format='md', extra_args=['--mathjax'])
    except RuntimeError:
        output = value
    return output


def parse_metadata(text):
    query = re.search(r'---\r\n(.*)\r\n---', text, re.DOTALL)
    if query:
        meta_raw = query.group(1)
        parts = meta_raw.split('\r\n')
        meta = {x[0]: x[1] for x in [x.split(':') for x in parts]}
        return meta
    return {}
