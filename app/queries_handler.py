import logging
import sqlalchemy
import app.error as error
import datetime
import re
from app.storage.db import db
from app.storage.book_titles import BookTitles
from app.storage.book_requests import BookRequests

log = logging.getLogger(__name__)

def add_book_title(title):
    '''
    add a book title to db
    '''
    new_title = BookTitles(title=title)
    try:
        db.session.add(new_title)
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as ex:
        db.session.rollback()
        log.error(f'sqlachemy error: {ex}')
        raise error.StorageError('could not add book title!')

    log.info(f'Book title {title} successfully added')
    return new_title

def get_book_title(book_title=None):
    '''
    get book titles from db
    '''
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
        log.error(f'Error while retrieving book title: {ex}')
        raise error.StorageError('Error while retrieving book title')


def _get_timestamp_now():
    '''
    get timestamp in in ISO 8601 format
    '''
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _check_email_address_format(email):
    '''
    an valid email address is a string (a subset of ASCII characters)
    separated into two parts by @ symbol, a “personal_info” and a domain
    followed by .domain_type
    e.g. personal_info@domain.net
    '''
    email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not (re.search(email_regex, email)):
        raise error.InvalidEmailFormat('Invalid email address format')


def create_book_request(email, title):
    '''
    validate and add a book request to db
    '''
    _check_email_address_format(email)
    title = get_book_title(title)
    timestamp = _get_timestamp_now()
    new_book_request = BookRequests(email=email, timestamp=timestamp, book_title=title)

    try:
        db.session.add(new_book_request)
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as ex:
        db.session.rollback()
        log.error(f'Could not add book request: {ex}')
        raise error.StorageError('Could not add book request!')

    ret_value = new_book_request.to_dict()
    ret_value['title'] = title.title
    log.info(f'new book request {ret_value} successfully added')
    return ret_value


def get_book_request(id_=None):
    '''
    get book requests from db
    '''
    query = db.session.query(BookRequests, BookTitles) \
            .join(BookRequests, BookTitles.id == BookRequests.book_title_id)
    try:
        if id_ is not None:
            query = query.filter(BookRequests.id == id_)
            res = query.one_or_none()
            if res is None:
                raise error.BookReqFoundError('Book request not found')
            book_req = res.BookTitles.to_dict()
            book_req.update(res.BookRequests.to_dict())

            return book_req
        else:
            req_list = query.all()

            ret_list = []
            for x in req_list:
                book_req_details = x.BookTitles.to_dict()
                book_req_details.update(x.BookRequests.to_dict())
                ret_list.append(book_req_details)

            return {'data': ret_list}

    except sqlalchemy.exc.SQLAlchemyError as ex:
        log.error(f'Error while retrieving book request: {ex}')
        raise error.StorageError('Error while retrieving book request')


def delete_book_request(id_):
    '''
    delete a book request by id
    '''
    try:
        book_req = BookRequests.get(id_)
        if book_req is None:
            raise error.BookReqFoundError('Book request not found')
        BookRequests.delete(id_)
    except sqlalchemy.exc.SQLAlchemyError as ex:
        log.error(f'Error while deleting book request {ex}')
        raise error.StorageError('Error while deleting book request')

    log.info(f'book request with id {id_} deleted')