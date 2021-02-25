import unittest
from main import create_app, db
from models.ProblemArea import ProblemArea


class TestAuthMoodApp(unittest.TestCase):
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

    def test_problemareas(self):
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

        response = self.client.get("/problem_area/problem_area_entries")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Problem Areas", str(response.data))

    def test_post_problemareas(self):
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

        response = self.client.post("/problem_area/new_entry", data={
            'problem_area_entry': 'test problem area',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Problem Areas", str(response.data))
        self.assertIn("test problem area", str(response.data))

    def test_delete_problemareas(self):
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

        response = self.client.post("/problem_area/new_entry", data={
            'problem_area_entry': 'test problem area',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Problem Areas", str(response.data))
        self.assertIn("test problem area", str(response.data))

        problem_entry = ProblemArea.query.first()
        response = self.client.post(f"problem_area/problem_area_entries/{problem_entry.id}",
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("test problem area", str(response.data))

    def test_get_problemarea(self):
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

        response = self.client.post("/problem_area/new_entry",
                                    data={
                                     'problem_area_entry': 'test problem area',
                                     }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Problem Areas", str(response.data))
        self.assertIn("test problem area", str(response.data))
        problem = ProblemArea.query.first()
        response = self.client.get(f"problem_area/problem_area_entry/{problem.id}",
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('test problem area', str(response.data))

    def test_get_all_problemareas(self):
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

        response = self.client.post("/problem_area/new_entry", data={
            'problem_area_entry': 'test problem area',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Problem Areas", str(response.data))
        self.assertIn("test problem area", str(response.data))

        problems = ProblemArea.query.all()
        response = self.client.get("problem_area/problem_area_entries")
        self.assertEqual(response.status_code, 200)
        self.assertIn("test problem area", str(response.data))
        self.assertIsInstance(problems, list)
