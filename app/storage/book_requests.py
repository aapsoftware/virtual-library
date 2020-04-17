import logging
import sqlalchemy
import string
import random
from app.storage.db import db

log = logging.getLogger(__name__)


def _get_random_string(number_of_chars, lower_case=False):
    """
    returns a random string of ascii chars and digits of a requested length
    """

    if lower_case:
        choice_string = string.ascii_lowercase + string.digits
    else:
        choice_string = string.ascii_letters + string.digits
    return ''.join([random.choice(choice_string) for _ in range(number_of_chars)])

def _get_unique_id():
        """
        get unique string id
        """
        id_ = _get_random_string(5)
        while db.session.query(BookRequests).filter(id == id_).limit(1).first() is not None:
            id_ = _get_random_string(5)

        return id_

class BookRequests(db.Model):
    """provides state information for plugins"""
    __tablename__ = 'BookRequests'

    id = db.Column(db.String, default=_get_unique_id, primary_key=True)
    book_title_id = db.Column(db.String, db.ForeignKey('BookTitles.id'), nullable=False)
    email = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)

    def __repr__(self):
        return (f'<id={self.id}, book_title_id={self.book_title_id}, '
                f'email={self.email}, timstamp={self.timestamp}>')

    def to_dict(self):
        """
        return dictionary representation
        """
        return {
            'id': self.id,
            'book_title_id': self.book_title_id,
            'email': self.email,
            'timestamp': self.timestamp
        }

    @classmethod
    def get(cls, request_id):
        """
        get a book request
        """
        return cls.query.filter_by(id=request_id).one_or_none()

    @classmethod
    def get_all(cls):
        """
        get all book titles
        """
        result = cls.query.all()
        return list(result)

    @classmethod
    def delete(cls, id_):
        """
        delete book request matching id
        """
        try:
            title = cls.query.filter_by(id=id_).one()
            db.session.delete(title)
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError:
            db.session.rollback()
            raise

    @classmethod
    def delete_all(cls):
        """
        delete all book titles
        """
        try:
            nr_deleted = db.session.query(cls).delete()
            db.session.commit()
            return nr_deleted
        except sqlalchemy.exc.SQLAlchemyError:
            db.session.rollback()
            raise
