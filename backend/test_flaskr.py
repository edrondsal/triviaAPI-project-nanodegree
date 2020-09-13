import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
import logging
import sys


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('udacity:udacity@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests for API Endpoints
    """
    def test_categories(self):
        log = logging.getLogger("TestLog")
        log.debug("test_categories")
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
    
    def test_category_questions(self):
        log = logging.getLogger("TestLog")
        log.debug("test_category_questions")
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

        res = self.client().get('/categories/200/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],'Not Found')

    def test_question_pagination(self):
        log = logging.getLogger("TestLog")
        log.debug("test_question_pagination")
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],'Not Found')        

    def test_search_question(self):
        log = logging.getLogger("TestLog")
        log.debug("test_search_question")
        res = self.client().post('/questions', json={'searchTerm': 'what'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

        res = self.client().post('/questions', json={'searchTerm': 'no item to found'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],'Not Found') 

    def test_create_question(self):
        log = logging.getLogger("TestLog")
        log.debug("test_create_question")
        res = self.client().post('/questions', json={'question': 'new question','answer': 'correct answer', 'difficulty': 5, 'category':2})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'],True)

        res = self.client().post('/questions', json={'question': 'new question','answer': 'correct answer'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],'unprocessable') 

    def test_delete_question(self):
        log = logging.getLogger("TestLog")
        log.debug("test_delete_question")
        questions = Question.query.all()
        question_id = questions[-1].id

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.get(question_id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
        self.assertEqual(question,None)

        res = self.client().delete('/questions/200')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],'unprocessable') 

    def test_play_game(self):
        log = logging.getLogger("TestLog")
        log.debug("test_play_game")
        res = self.client().post('/quizzes', json={'quiz_category': {'id': '2'},'previous_questions': []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])

        res = self.client().post('/quizzes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],'unprocessable')    

        res = self.client().post('/quizzes',json={'quiz_category': {'type':'sometype'},'previous_questions': []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],'unprocessable')  

        res = self.client().post('/quizzes',json={'quiz_category': {'id': '2'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],422)
        self.assertEqual(data['message'],'unprocessable')      

# Make the tests conveniently executable
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main()