"""Fix image URL paths.
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
    glosses = db.session.query(models.Gloss).all()
    for gloss in glosses:
        text = gloss.text_
        print(text)
        db.session.merge(gloss)
    db.session.commit()
