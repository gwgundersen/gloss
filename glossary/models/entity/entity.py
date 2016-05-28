"""Represent an annotatable entity in the program."""

from glossary import db


class Entity(db.Model):

    __tablename__ = 'entity'
    id = db.Column(db.Integer, primary_key=True)
    type_ = db.Column(db.String(255))
    glosses = db.relationship('Gloss', backref='entity',
                              order_by='desc(Gloss.timestamp)')

    __mapper_args__ = {
        'polymorphic_identity': 'entity',
        'polymorphic_on': type_
    }

    @property
    def endpoint(self):
        return 'entity/%s' % self.id

    @classmethod
    def stats(cls):
        return None

    @property
    def labels(self):
        label_names = []
        _labels = []
        for gloss in self.glosses:
            for label in gloss.labels:
                if label.name in label_names:
                    continue
                label_names.append(label.name)
                _labels.append(label)
        return _labels
