import flask

import app.error as error
from test.base import BaseTestCase
from app.storage.book_titles import BookTitles
from app.storage.book_requests import BookRequests
from app.storage.db import db


class TestRequestApi(BaseTestCase):
    """Request test stubs"""

    def setUp(self):
        '''called bofore each test method'''
        new_title1 = BookTitles(title='Book Title 1')
        new_title2 = BookTitles(title='Book Title 2')
        new_title3 = BookTitles(title='Book Title 3')

        db.session.add(new_title1)
        db.session.add(new_title2)
        db.session.add(new_title3)
        db.session.commit()

    def tearDown(self):
        '''called after each test method'''
        db.session.remove()
        db.drop_all()


    def test_add_book_request(self):
        book_title = "Book Title 1"
        email = "me@testing.com"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )

        self.assertStatus(response, 200)
        data = response.json

        self.assertEqual(len(data), 4)
        self.assertIn('id', data)
        self.assertIn('timestamp', data)
        self.assertEqual(data['title'], book_title)
        self.assertEqual(data['email'], email)

        all_books_requests = BookRequests.get_all()
        self.assertEqual(len(all_books_requests), 1)

    def test_create_book_request_book_not_found(self):
        book_title = "Book Title"
        email = "me@testing.com"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )

        self.assertStatus(response, 404)

        all_books_requests = BookRequests.get_all()
        self.assertEqual(len(all_books_requests), 0)

    def test_create_book_request_invalid_email1(self):
        book_title = "Book Title"
        email = "me@testing"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )

        self.assertStatus(response, 400)

        all_books_requests = BookRequests.get_all()
        self.assertEqual(len(all_books_requests), 0)

    def test_create_book_request_invalid_email2(self):
        book_title = "Book Title"
        email = "me;@testing.com"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )

        self.assertStatus(response, 400)

        all_books_requests = BookRequests.get_all()
        self.assertEqual(len(all_books_requests), 0)

    def test_create_book_request_invalid_email3(self):
        book_title = "Book Title"
        email = "me@testing.coms"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )

        self.assertStatus(response, 400)

        all_books_requests = BookRequests.get_all()
        self.assertEqual(len(all_books_requests), 0)

    def test_create_book_request_invalid_email4(self):
        book_title = "Book Title"
        email = "metesting.com"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )

        self.assertStatus(response, 400)

        all_books_requests = BookRequests.get_all()
        self.assertEqual(len(all_books_requests), 0)

    def test_get_book_request(self):
        book_title = "Book Title 1"
        email = "me@testing.com"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )
        self.assertStatus(response, 200)
        req_id = response.json['id']

        response = self.client.open(
            '/api/v1/request/{}'.format(req_id),
            method='GET',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )
        self.assertStatus(response, 200)
        data = response.json

        self.assertEqual(len(data), 4)
        self.assertIn('id', data)
        self.assertIn('timestamp', data)
        self.assertEqual(data['title'], book_title)
        self.assertEqual(data['email'], email)

    def test_get_book_request_not_found(self):
        book_title = "Book Title 1"
        email = "me@testing.com"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )
        self.assertStatus(response, 200)

        response = self.client.open(
            '/api/v1/request/{}'.format('test'),
            method='GET',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )
        self.assertStatus(response, 404)

    def test_get_all_book_requests(self):
        book_title = "Book Title 1"
        email = "me@testing.com"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )
        self.assertStatus(response, 200)

        book_title = "Book Title 2"
        email = "me@testing.com"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )
        self.assertStatus(response, 200)

        book_title = "Book Title 3"
        email = "me@testing.com"
        response = self.client.open(
            '/api/v1/request',
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
            query_string=[('email', email), ('title', book_title)]
        )
        self.assertStatus(response, 200)

        response = self.client.open(
            '/api/v1/request',
            method='GET',
            content_type='application/json',
            headers={'accept': 'application/json'}
        )
        self.assertStatus(response, 200)
        data = response.json['data']
        self.assertEqual(len(data), 3)

    def test_get_all_book_requests_empty_db(self):
        BookTitles.delete_all()

        response = self.client.open(
            '/api/v1/request',
            method='GET',
            content_type='application/json',
            headers={'accept': 'application/json'}
        )
        self.assertStatus(response, 200)
        data = response.json['data']
        self.assertEqual(data, [])