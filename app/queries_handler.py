import logging
import sqlalchemy
import app.error as error
import datetime
from app.storage.db import db
from app.storage.book_titles import BookTitles
from app.storage.book_requests import BookRequests


log = logging.getLogger(__name__)

def add_book_title(title):
    new_title = BookTitles(title=title)
    try:
        db.session.add(new_title)
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as ex:
        db.session.rollback()
        log.error(f'sqlachemy error: {ex}')
        raise error.StorageError('could not add book title!')

    return new_title

def get_book_title(book_title=None):
    try:
        if book_title is not None:
            title = BookTitles.get(book_title)
            if title is None:
                raise error.TitleNotFoundError('Title not found')
            return title
        else:
            title_list = BookTitles.get_all()
            return {'data': title_list}

    except sqlalchemy.exc.SQLAlchemyError as ex:
        raise error.StorageError('Error while retrieving book title')


def _get_timestamp_now():
    TIME_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    datetime_as_str = datetime.datetime.now().strftime(TIME_DATE_FORMAT)
    return datetime.datetime.strptime(datetime_as_str,TIME_DATE_FORMAT)

def create_book_request(email, title):
    title = get_book_title(title)
    timestamp = _get_timestamp_now()
    new_book_request = BookRequests(email=email, timestamp=timestamp, book_title=title)

    try:
        db.session.add(new_book_request)
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as ex:
        db.session.rollback()
        log.error(f'sqlachemy error: {ex}')
        raise error.StorageError('could not add book request!')

    return new_book_request

def get_book_request(id_=None):
    try:
        if id_ is not None:
            book_req = BookRequests.get(id_)
            if book_req is None:
                raise error.BookReqFoundError('Book request not found')
            return book_req
        else:
            req_list = BookRequests.get_all()
            return {'data': req_list}

    except sqlalchemy.exc.SQLAlchemyError as ex:
        raise error.StorageError('Error while retrieving book request')


def delete_book_request(id_):
    try:
        book_req = BookRequests.get(id_)
        if book_req is None:
            raise error.BookReqFoundError('Book request not found')
        BookRequests.delete(id_)
    except sqlalchemy.exc.SQLAlchemyError:
        raise error.StorageError('Error while deleting request')