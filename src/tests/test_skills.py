import unittest
from main import create_app, db
from models.Skill import Skill


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

    def test_skills(self):
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

        response = self.client.get("/skill/skill_entries")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Skills", str(response.data))

    def test_post_skills(self):
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

        response = self.client.post("/skill/new_entry", data={
            'skill_entry': 'test skill',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Skills", str(response.data))
        self.assertIn("test skill", str(response.data))

    def test_delete_skills(self):
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

        response = self.client.post("/skill/new_entry", data={
            'skill_entry': 'test skill',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Skills", str(response.data))
        self.assertIn("test skill", str(response.data))

        skill_entry = Skill.query.first()
        response = self.client.post(f"skill/skill_entries/{skill_entry.id}",
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("test skill", str(response.data))

    def test_get_skill(self):
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

        response = self.client.post("/skill/new_entry", data={
            'skill_entry': 'test skill',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Skills", str(response.data))
        self.assertIn("test skill", str(response.data))

        skill = Skill.query.first()
        response = self.client.get(f"skill/skill_entry/{skill.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('test skill', str(response.data))

    def test_get_all_skill(self):
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

        response = self.client.post("/skill/new_entry", data={
            'skill_entry': 'test skill',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Skills", str(response.data))
        self.assertIn("test skill", str(response.data))

        skills = Skill.query.all()
        response = self.client.get("skill/skill_entries")
        self.assertEqual(response.status_code, 200)
        self.assertIn('test skill', str(response.data))
        self.assertIsInstance(skills, list)
