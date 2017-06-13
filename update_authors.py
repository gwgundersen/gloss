"""Update author names.
"""

import argparse
from flask_sqlalchemy import SQLAlchemy
from gloss import models, app


db = SQLAlchemy()


parser = argparse.ArgumentParser()
parser.add_argument('--user',     required=True,  type=str)
parser.add_argument('--passwd',   required=True,  type=str)
parser.add_argument('--host',     required=True,  type=str)
parser.add_argument('--database', required=True,  type=str)
args = parser.parse_args()


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s:3306/%s" % (
    args.user, args.passwd, args.host, args.database
)


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
