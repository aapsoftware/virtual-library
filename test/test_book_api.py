import flask

import app.error as error
from test.base import BaseTestCase
from app.storage.book_titles import BookTitles
from app.storage.db import db


class TestBookApi(BaseTestCase):
    """Book test stubs"""

    def tearDown(self):
        '''called after each test method'''
        db.session.remove()
        db.drop_all()


    def test_add_book(self):
        book_title ="Just For Testing"
        response = self.client.open(
            '/api/v1/book/{}'.format(book_title),
            method='POST',
            content_type='application/json',
            headers={'accept': 'application/json'},
        )

        self.assertStatus(response, 200)
        data = response.json

        self.assertEqual(len(data), 2)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], book_title)

        all_books = BookTitles.get_all()
        self.assertEqual(len(all_books), 1)
        self.assertEqual(str(all_books[0]), f'<id=1, title={book_title}>')


    def test_add_book_error_method_not_allowed(self):
        book_title ="Just For Testing"
        response = self.client.open(
            '/api/v1/book',
            method='POST'
        )
        self.assertStatus(response, 405)


    def test_get_book(self):
        book_title ="Just For Testing"
        response = self.client.open(
            '/api/v1/book/{}'.format(book_title),
            method='POST'
        )
        self.assertStatus(response, 200)

        response = self.client.open(
            '/api/v1/book/{}'.format(book_title),
            method='GET'
        )
        self.assertStatus(response, 200)

        data = response.json
        self.assertEqual(len(data), 2)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], book_title)


    def test_get_book_not_found(self):
        book_title ="Just For Testing"
        response = self.client.open(
            '/api/v1/book/{}'.format(book_title),
            method='POST'
        )
        self.assertStatus(response, 200)

        response = self.client.open(
            '/api/v1/book/{}'.format('book_title'),
            method='GET'
        )
        self.assertStatus(response, 404)


    def test_get_books_emptydb(self):
        response = self.client.open(
            '/api/v1/book',
            method='GET'
        )
        self.assertStatus(response, 204)


    def test_get_books(self):
        book_title ="Just For Testing vol1"
        response = self.client.open(
            '/api/v1/book/{}'.format(book_title),
            method='POST'
        )
        self.assertStatus(response, 200)
        book_title ="Just For Testing vol2"
        response = self.client.open(
            '/api/v1/book/{}'.format(book_title),
            method='POST'
        )
        self.assertStatus(response, 200)
        book_title ="Just For Testing vol3"
        response = self.client.open(
            '/api/v1/book/{}'.format(book_title),
            method='POST'
        )
        self.assertStatus(response, 200)

        response = self.client.open(
            '/api/v1/book',
            method='GET'
        )
        self.assertStatus(response, 200)

        data = response.json['data']
        self.assertEqual(len(data), 3)
        expected_books = [
            {'id': 1, 'title': 'Just For Testing vol1'},
            {'id': 2, 'title': 'Just For Testing vol2'},
            {'id': 3, 'title': 'Just For Testing vol3'}
        ]
        self.assertEqual(data, expected_books)
