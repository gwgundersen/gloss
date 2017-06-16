"""Search engine for glosses.
"""

from sqlalchemy import text

from gloss import db, models


def find_glosses_by_keyword(keyword):
    """Return glosses based on keyword matches."""
    keyword = _preprocess_keyword(keyword)
    print(keyword)
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
    sql = 'SELECT id FROM gloss WHERE MATCH (text_) AGAINST (:keyword IN BOOLEAN MODE)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    return [int(g[0]) for g in t]


def _find_gloss_ids_by_titles(keyword):
    """Return gloss IDs based on keyword matches in entity titles.
    """
    ids = []

    sql = 'SELECT gloss.id FROM gloss '\
          '  JOIN book ON book.entity_fk = gloss.entity_fk '\
          'WHERE MATCH (book.title) AGAINST (:keyword IN BOOLEAN MODE)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids += [int(g[0]) for g in t]

    sql = 'SELECT gloss.id FROM gloss '\
          '  JOIN paper ON paper.entity_fk = gloss.entity_fk '\
          'WHERE MATCH (paper.title) AGAINST (:keyword IN BOOLEAN MODE)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids += [int(g[0]) for g in t]

    sql = 'SELECT gloss.id FROM gloss '\
          '  JOIN talk ON talk.entity_fk = gloss.entity_fk '\
          'WHERE MATCH (talk.title) AGAINST (:keyword IN BOOLEAN MODE)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids += [int(g[0]) for g in t]

    sql = 'SELECT gloss.id FROM gloss '\
          '  JOIN website ON website.entity_fk = gloss.entity_fk '\
          'WHERE MATCH (website.title) AGAINST (:keyword IN BOOLEAN MODE)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids += [int(g[0]) for g in t]

    return ids


def _find_gloss_ids_by_author(keyword):
    """Return gloss IDs based on keyword matches in text.
    """
    ids = []

    # Find authors of books.
    sql = 'SELECT gloss.id FROM gloss '\
          '  JOIN author_to_book ON author_to_book.book_fk = gloss.entity_fk '\
          '  JOIN author ON author.id = author_to_book.author_fk '\
          'WHERE MATCH (author.name) AGAINST (:keyword IN BOOLEAN MODE)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids += [int(g[0]) for g in t]

    # Find authors of papers.
    sql = 'SELECT gloss.id FROM gloss '\
          '  JOIN author_to_paper ON author_to_paper.paper_fk = gloss.entity_fk '\
          '  JOIN author ON author.id = author_to_paper.author_fk '\
          'WHERE MATCH (author.name) AGAINST (:keyword IN BOOLEAN MODE)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids += [int(g[0]) for g in t]

    # Find authors of talks.
    sql = 'SELECT gloss.id FROM gloss '\
          '  JOIN author_to_talk ON author_to_talk.talk_fk = gloss.entity_fk '\
          '  JOIN author ON author.id = author_to_talk.author_fk '\
          'WHERE MATCH (author.name) AGAINST (:keyword IN BOOLEAN MODE)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids += [int(g[0]) for g in t]

    # Find authors of websites.
    sql = 'SELECT gloss.id FROM gloss '\
          '  JOIN author_to_website ON author_to_website.website_fk = gloss.entity_fk '\
          '  JOIN author ON author.id = author_to_website.author_fk '\
          'WHERE MATCH (author.name) AGAINST (:keyword IN BOOLEAN MODE)'
    conn = db.engine.connect()
    t = conn.execute(text(sql), keyword=keyword)
    ids += [int(g[0]) for g in t]
    return ids


def _preprocess_keyword(keyword):
    """Prepare keyword for IN BOOLEAN MODE.
    """
    # parts = ['+' + x for x in keyword.split()]
    # return ' '.join(parts)
    return keyword

