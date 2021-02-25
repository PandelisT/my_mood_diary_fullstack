import unittest
from main import create_app, db
from models.Psychologist import Psychologist


class TestPsychMoodApp(unittest.TestCase):
    @classmethod
    def setUp(cls):
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

    def test_post_psych(self):
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

        response = self.client.post("/psychologist/new_details", data={
            'email': 'test@test.com',
            'name': 'Testing',
            'user_id': 1
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Profile", str(response.data))

    def test_get_psych(self):
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

        response = self.client.post("/psychologist/new_details", data={
            'email': 'test@test.com',
            'name': 'Testing',
            'user_id': 1
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Profile", str(response.data))

        psych = Psychologist.query.all()
        response = self.client.get("/psychologist/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(psych, list)
