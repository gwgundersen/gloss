"""Represent a gloss annotating an entity."""

from glossary import db, config


class Gloss(db.Model):

    __tablename__ = 'gloss'
    id        = db.Column(db.Integer, primary_key=True)
    entity_fk = db.Column(db.Integer, db.ForeignKey('entity.id'),
                           nullable=True)
    title     = db.Column(db.String(255), nullable=True)
    text_     = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    archive   = db.Column(db.Boolean, nullable=False, default=False)
    labels    = db.relationship('Label', backref='glosses',
                                 secondary='label_to_gloss')

    @property
    def endpoint(self):
        return 'gloss'

    @property
    def labels_alpha(self):
        """Returns gloss's labels alphabetically sorted."""
        return sorted(self.labels, key=lambda x: x.name)

    @property
    def is_public(self):
        """Returns True if the gloss should be viewable to the public."""
        return 'public' in [l.name for l in self.labels]

    @property
    def public_url(self):
        if not self.is_public:
            return ''
        path = config.get('url', 'public')
        title = self.title.replace(' ', '_').lower()
        return '%s/%s/%s' % (path, self.id, title)
