"""
Book API - to be used mainly for testing and populating the db with book titles
"""
import logging

from flask_restplus import Resource
from app.rest import flask_api
import app.serializers as serializers
import app.queries_handler as qh

log = logging.getLogger(__name__)

ns = flask_api.namespace('book', validate=True, description=__doc__)

@ns.route('')
class Book_title_all(Resource):
    @ns.doc('retrieve_all_book_titles')
    @ns.marshal_with(serializers.book_title_list, skip_none=True)
    @ns.response(200, 'Book titles retuned successfully')
    @ns.response(204, 'No Book titles')
    @ns.response(400, 'Error retrieving book titles')
    def get(self):
        """
        get all book titles
        """
        titles_data = qh.get_book_title()
        if not titles_data["data"]:
            return {}, 204
        return titles_data

@ns.route('/<book_title>')
@ns.param('book_title', 'book title')
class Book_titles(Resource):
    @ns.doc('add_book_title')
    @ns.marshal_with(serializers.book_title, skip_none=True)
    @ns.response(200, 'Book title added successfully')
    @ns.response(400, 'Error when storing book stitle')
    def post(self, book_title):
        """
        add a book title
        """
        return qh.add_book_title(book_title)

    @ns.doc('retrieve_book_title')
    @ns.marshal_with(serializers.book_title, skip_none=True)
    @ns.response(200, 'Book title returned sucessfully')
    @ns.response(404, 'Book title not found')
    @ns.response(400, 'Error retrieving book title')
    def get(self, book_title):
        """
        get book by title
        """
        return qh.get_book_title(book_title)
