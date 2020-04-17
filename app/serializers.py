import flask_restplus
import app.rest as rest

book_request = rest.flask_api.model('book_request', {
    'email': flask_restplus.fields.String(example='me@email.com'),
    'title': flask_restplus.fields.String(example='The three little pigs'),
    'id': flask_restplus.fields.String(example='hfg3s'),
    'timestamp': flask_restplus.fields.String(
        description='Request timestamp in ISO 8601 format', example='2020-01-01T23:30:00'
    )
})

book_request_list = rest.flask_api.model('book_request_list', {
    'data': flask_restplus.fields.List(flask_restplus.fields.Nested(book_request, skip_none=True))
})

book_title = rest.flask_api.model('book_title', {
    'id': flask_restplus.fields.Integer(example='1'),
    'title': flask_restplus.fields.String(example='Alone in the woods'),
})

book_title_list = rest.flask_api.model('book_title_list', {
    'data': flask_restplus.fields.List(flask_restplus.fields.Nested(book_title, skip_none=True))
})