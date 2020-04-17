import logging
import sqlalchemy

from app.storage.db import db

log = logging.getLogger(__name__)

class BookTitles(db.Model):
    """provides state information for plugins"""
    __tablename__ = 'BookTitles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    book_request = db.relationship('BookRequests', backref="book_title", single_parent=True,
                                    cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f'<id={self.id}, title={self.title}>'


    def to_dict(self):
        """
        return dictionary representation
        """
        return {'id': self.id, 'title': self.title}


    @classmethod
    def get(cls, book_title):
        """
        get a book title
        """
        return cls.query.filter_by(title=book_title).one_or_none()

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
        delete book title matching id
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
