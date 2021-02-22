import unittest
import os
from main import create_app, db
from models.Journal import Journal


class TestAuthMoodApp(unittest.TestCase):
    @classmethod
    def setUp(cls):
        if os.environ.get("FLASK_ENV") != ("testing" or "workflow"):
            raise EnvironmentError("FLASK_ENV is not testing")
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_journal(self):
        response = self.client.post('/signup', data={
            'email': 'pandeli@test.com',
            'name': 'Pandelis',
            'password': 'testing'
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login', data={
            'email': 'pandeli@test.com',
            'password': 'testing'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/journal/journal-entries")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Journal entries", str(response.data))

    def test_post_journal(self):
        response = self.client.post('/signup', data={
            'email': 'pandeli@test.com',
            'name': 'Pandelis',
            'password': 'testing'
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login', data={
            'email': 'pandeli@test.com',
            'password': 'testing'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/journal/new_entry", data={
            'journal_entry': 'test entry',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Journal entries", str(response.data))
        self.assertIn("test entry", str(response.data))

    def test_delete_journal(self):
        response = self.client.post('/signup', data={
            'email': 'pandeli@test.com',
            'name': 'Pandelis',
            'password': 'testing'
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/login', data={
            'email': 'pandeli@test.com',
            'password': 'testing'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/journal/new_entry", data={
            'journal_entry': 'test entry',
        }, follow_redirects=True)

        journal_entry = Journal.query.first()
        response = self.client.post(f"journal/journal-entries/{journal_entry.id}", follow_redirects=True)
               
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("test entry", str(response.data))
