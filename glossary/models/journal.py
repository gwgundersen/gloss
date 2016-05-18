"""Represent a scientific journal."""

from glossary import db


class Journal(db.Model):

    __tablename__ = 'journal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    @property
    def name_as_url(self):
        return self.name.replace(' ', '_')
