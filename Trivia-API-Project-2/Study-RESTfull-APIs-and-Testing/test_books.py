import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from bookshelf import *
from models import *



class BookTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client

        database_path = "postgresql://{}:{}@{}/{}".format('postgres', '1','localhost:5432', "test_bookshelf")
        setup_db(self.app,database_path)


    def tearDown(self):
        return super().tearDown()

    def test_getAllBooks(self):
        res = self.client().get('/books')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
    
    def test_deleteBook(self):
        print(Book.query.all())
        res = self.client().delete("/books/1")
        data = json.loads(res.data)
        self.assertTrue( data['success'] )

        book = Book(title="Book1",id=1)
        book.insert()

    def test_patchBook(self):
        res = self.client().patch("/books/3" ,json={"rating" : "55"})
        print("RESPONSE : ", res)
        data = json.loads( res.data )
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])

        # self.client().patch("books/3" ,json= {"title" : "S"})

    def test_404_not_found_json_patchBook(self):
        res = self.client().patch("/books/3" )
        data = json.loads( res.data )
        self.assertEqual(res.status_code,400)
        self.assertFalse(data['success'])


    def test_search_with_result_book(self):
        res = self.client().get('/books?search=am')
        data = json.loads(res.data)

        self.assertEqual(res.status_code ,200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['books']))
        for book in data['books']:
            found = book['title'].find('am') != 0
            self.assertTrue(found)

    def test_search_without_result_book(self):
        res = self.client().get('/books?search=zzzzzzzzzzz')
        data = json.loads(res.data)

        self.assertEqual(res.status_code ,200)
        self.assertTrue(data['success'])
        self.assertFalse(len(data['books']))


if __name__ == "__main__" :
    unittest.main()
