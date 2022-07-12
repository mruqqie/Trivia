import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.database_user = DB_USER
        self.database_password = DB_PASSWORD
        self.database_path = "postgresql://{}:{}@{}/{}".format(
                        self.database_user, self.database_password,
                        "localhost:5432", self.database_name
                        )

        #self.database_name = "trivia_test"
        #self.database_path = 'postgresql://postgres:postgres@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "What is Rachel's surname in FRIENDS?",
            "answer": "Green",
            "difficulty": 1,
            "category": 5
        }

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
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_category"])

    def fail_get_categories(self):
        red = self.client().get("/categories/5000")
        data - json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual["message"], "Resource not found"

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_get_questions_with_invalid_page(self):
        res = self.client().get("/questions?page=1000000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_delete_question(self):
        res = self.client().delete("/questions/23")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 23).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 23)
        self.assertTrue(data["total_questions"])
        self.assertEqual(question, None)

    def test_delete_question_fail(self):
        res = self.client().delete("/questions/500000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    def test_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])

    def fail_to_create_new_question(self):
        res = self.client().post("/questions/50")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

    def test_search_question(self):
        res = self.client().post('/questions/search', json={"searchTerm": "w"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def fail_search_question(self):
        res = self.client().post('/questions/search',
                                 json={"search": "wqerrt"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_get_questions_by_cat(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def fail_get_questions_by_cat(self):
        res = self.client().get("/categories/67yg/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_get_quiz_questions(self):
        res = self.client().post("/quizzes",
                                 json={"previous_questions": 16,
                                       "quiz_category": {'type': 'Art', 'id': 2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def fail_get_quiz_questions(self):
        res = self.client().post("/quizzes",
                                 json={"previous_questions": 16,
                                       "quiz_category": {'type': 'Art', 'id': 60}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
