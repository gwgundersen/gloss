"""Functions for rendering Markdown and LaTeX as HTML.
"""

import pypandoc


def render_markdown(value):
    """Render Markdown"""
    try:
        output = pypandoc.convert_text(value, to='html5', format='md', extra_args=['--mathjax'])
    except RuntimeError:
        output = value
    return output
