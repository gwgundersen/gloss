"""Update author names.
"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from gloss import models, app


with app.app_context():
    authors = db.session.query(models.Author).all()
    for auth in authors:
        if not auth.name:
            db.session.delete(auth)
            continue
        if auth.name.lower() == 'foo bar':
            db.session.delete(auth)
            continue
        new_name = []
        for part in auth.name.split():
            new_name.append(part.capitalize())
        new_name = ' '.join(new_name)
        auth.name = new_name
        db.session.merge(auth)
    db.session.commit()
