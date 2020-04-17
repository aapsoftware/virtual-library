"""
Book Request API
"""
import logging

from flask_restplus import Resource
from app.rest import flask_api
import app.serializers as serializers
import app.queries_handler as qh

log = logging.getLogger(__name__)

ns = flask_api.namespace('request', validate=True, description=__doc__)

book_req_params = ns.parser()
book_req_params.add_argument('email', type=str, help='user_email', location='values', dest='email', required=True)
book_req_params.add_argument('title', type=str, help='book title', location='values', dest='title', required=True)

@ns.route('')
class Request(Resource):
    @ns.doc('request_book')
    @ns.expect(book_req_params, validate=True)
    @ns.marshal_with(serializers.book_request, skip_none=True)
    @ns.response(200, 'Request successful')
    @ns.response(400, 'Request error')
    def post(self):
        """
        create a book request
        """
        args = book_req_params.parse_args()
        return qh.create_book_request(email=args['email'], title=args['title'])


    @ns.doc('retrieve_all_book_requests')
    @ns.marshal_with(serializers.book_request_list, skip_none=True)
    @ns.response(200, 'Request successful')
    @ns.response(404, 'Request not found')
    @ns.response(400, 'Request error')
    def get(self):
        """
        get all book requests
        """
        return qh.get_book_request()

@ns.route('/<id>')
@ns.param('id', 'request id')
class Request_with_id(Resource):
    @ns.doc(id='retrieve_book_request')
    @ns.marshal_with(serializers.book_request, skip_none=True)
    @ns.response(200, 'Request successful')
    @ns.response(404, 'Request not found')
    @ns.response(400, 'Request error')
    def get(self, id):
        """
        get a book request by id
        """
        return qh.get_book_request(id)

    @ns.doc(id='delete_book_request')
    @ns.response(200, 'Request deleted successfully')
    @ns.response(404, 'Request not found')
    @ns.response(400, 'Request error')
    def delete(self, id):
        """
        delete a book request
        """
        qh.delete_book_request(id)
        return 200
