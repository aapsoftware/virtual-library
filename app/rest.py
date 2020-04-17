import logging
import werkzeug.exceptions
import flask_restplus

import app.error as err

log = logging.getLogger(__name__)

flask_api = flask_restplus.Api(
    version='1.0',
    title='Book Request API',
    description='A book request API for a thoretical virtual library',
    default='request',
    default_label='',
    ordered=False,
    ui='/'
)

@flask_api.errorhandler(err.StorageError)
@flask_api.errorhandler(err.InvalidEmailFormat)
def handle_storage_error(error):
    """Storage Errors"""
    http_status = 400
    if isinstance(error, err.TitleNotFoundError) or isinstance(error, err.BookReqFoundError):
        http_status = 404

    return {'error': {'message': str(error)}}, http_status


@flask_api.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(error):
    """Invalid Request"""
    return {'error': {'message': str(error)}}, 400


@flask_api.errorhandler(werkzeug.exceptions.NotFound)
def handle_not_found(error):
    """Not Found"""
    return {'error': {'message': str(error)}}, 404


@flask_api.errorhandler
def handle_default_error(error):
    """Internal processing error"""
    log.exception('An unhandled exception occurred. %s', str(error))

    return {'error': {'code': 500, 'message': "An internal error occurred"}}, 500
