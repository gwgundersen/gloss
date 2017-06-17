"""Search engine for glosses.
"""

from gloss import db, models


def find_glosses_by_keyword(keyword):
    """Return glosses based on keyword matches."""
    keyword = _preprocess_keyword(keyword)
    ids = []
    ids += _find_gloss_ids_by_text(keyword)
    ids += _find_gloss_ids_by_author(keyword)
    ids += _find_gloss_ids_by_titles(keyword)
    # Make list of IDs unique to prevent duplicates.
    ids = set(ids)
    glosses = db.session.query(models.Gloss)\
        .filter(models.Gloss.id.in_(ids))\
        .order_by(models.Gloss.timestamp.desc())\
        .all()
    return glosses


def _find_gloss_ids_by_text(keyword):
    """Return gloss IDs based on keyword matches in text.
    """
    ids = db.session.query(models.Gloss.id)\
        .filter(models.Gloss.text_.match(keyword))\
        .all()
    return [t[0] for t in ids]


def _find_gloss_ids_by_titles(keyword):
    """Return gloss IDs based on keyword matches in entity titles.
    """
    ids = []

    ids += db.session.query(models.Gloss.id)\
        .join(models.Book)\
        .filter(models.Book.title.match(keyword))\
        .all()

    ids += db.session.query(models.Gloss.id)\
        .join(models.Paper)\
        .filter(models.Paper.title.match(keyword))\
        .all()

    ids += db.session.query(models.Gloss.id)\
        .join(models.Talk)\
        .filter(models.Talk.title.match(keyword))\
        .all()

    ids += db.session.query(models.Gloss.id)\
        .join(models.Website)\
        .filter(models.Website.title.match(keyword))\
        .all()

    return [t[0] for t in ids]


def _find_gloss_ids_by_author(keyword):
    """Return gloss IDs based on keyword matches in text.
    """
    ids = []

    # Find authors of books.
    ids += db.session.query(models.Gloss.id)\
        .join(models.Book)\
        .join(models.author_to_book)\
        .join(models.Author)\
        .filter(models.Author.name.match(keyword))\
        .all()

    # Find authors of papers.
    ids += db.session.query(models.Gloss.id)\
        .join(models.Paper)\
        .join(models.author_to_paper)\
        .join(models.Author)\
        .filter(models.Author.name.match(keyword))\
        .all()

    # Find authors of talks.
    ids += db.session.query(models.Gloss.id)\
        .join(models.Talk)\
        .join(models.author_to_talk)\
        .join(models.Author)\
        .filter(models.Author.name.match(keyword))\
        .all()

    # Find authors of websites.
    ids += db.session.query(models.Gloss.id)\
        .join(models.Website)\
        .join(models.author_to_website)\
        .join(models.Author)\
        .filter(models.Author.name.match(keyword))\
        .all()

    return [t[0] for t in ids]


def _preprocess_keyword(keyword):
    """Prepare keyword for IN BOOLEAN MODE.
    """
    return '"' + keyword + '"'

