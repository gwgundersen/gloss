"""Represents application user."""

import hashlib
import uuid

from sqlalchemy.orm.exc import NoResultFound

from gloss import db


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    hashed_pw = db.Column(db.String(255))
    salt = db.Column(db.String(255))

    def __init__(self, name, password, active=True):
        self.name = name
        hashed_pw, salt = User.hash_password(password)
        self.hashed_pw = hashed_pw
        self.salt = salt
        self.active = active

    # Used by flask_login.
    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        # The user will fail to be constructed if not valid. Therefore, all
        # instances of the User class are authenticated.
        return True

    def is_correct_password(self, candidate):
        """
        Returns True if the candidate password is correct, False otherwise.
        """
        return hashlib.sha512(candidate + self.salt)\
                   .hexdigest() == self.hashed_pw

    @staticmethod
    def hash_password(password):
        """Hash a password for the first time."""
        salt = uuid.uuid4().hex
        hashed_pw = hashlib.sha512(password + salt).hexdigest()
        return hashed_pw, salt

    @classmethod
    def get(cls, username, candidate_pw):
        """
        Returns user by name if they exist and the provided password is
        correct. Returns None otherwise.
        """
        try:
            user = db.session.query(cls).filter(cls.name == username).one()
        except NoResultFound:
            return None
        if user.is_correct_password(candidate_pw):
            return user
        return None
