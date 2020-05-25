import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
from flask import jsonify

from __init__ import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_trivia"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '1','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_getCategories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['success'])
        self.assertGreater(data['total_categories'],0)

    def test_getQuestions_without_page(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertGreater(data['totalQuestions'],0)
        self.assertIsNone(data['currentCategory'])

    def test_getQuestions_with_page(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertGreater(data['totalQuestions'],0)
        self.assertIsNone(data['currentCategory'])


    def test_getQuestions_with_wrong_page(self):
        # res = self.client().get('/questions?page=1000')
        # data = json.loads(res.data)

        # self.assertEqual(res.status_code,422)
        # self.assertFalse(data['success'])
        # self.assertEqual(data['error'],422)
        pass

    def test_deleteCategories(self):
        res = self.client().delete('/questions/22')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])

        question = Question("TestDeleteQuestion","TestDeleteAnswer",3,3)
        question.setID(22)
        question.insert()
    
    def test_deleteCategories_with_wrong_id(self):
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'],400)
    
    def test_addQuestion(self):
        res = self.client().post('/questions', json = {
        'question': "testAddQuestion",
        'answer':  "testAnswerQuestion",
        'difficulty': 3,
        'category' :3 
        }        )
        json_res = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(json_res['success'])
        self.assertIsNotNone(json_res['id'])

        delete_question = Question.query.get(json_res['id'])
        delete_question.delete()
    
    def test_searchQuestion(self):        
        res = self.client().post('/questions', json =  { "searchTerm": "title" })
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])

        self.assertTrue(data['questions'])
        self.assertIsNone(data['currentCategory'])
        

    def test_PostQuestion_without_json(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'],400)

    
    def test_getCategoryQuestions(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])

        self.assertTrue(data['questions'])
        self.assertGreater(data['totalQuestions'],0)
        self.assertIsNone(data['currentCategory'])

    def test_getCategories_with_wrong_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'],404)


    def test_getQuizzes(self):
        data = {
            "quiz_category" : {"id" : 2} ,
            "previous_questions" : [16,17]
        }

        res = self.client().post('/quizzes', json = data)
        json_res = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(json_res['success'])

        # the answer will be random of 18 or 19
        self.assertGreaterEqual(json_res['question']['id'],18)
        self.assertLessEqual(json_res['question']['id'],19)

    def test_getQuizzes_with_no_remain_questions(self):
        res = self.client().post('/quizzes', json = {
            'quiz_category' : {"id" : 2} ,
            'previous_questions': [16,17,18,19]
        }
        )
        json_res = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertIsNone(json_res['question'])


    def test_getQuizzes_without_json(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'],400)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()