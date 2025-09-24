import unittest
from backend.app import app

class BasicApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_health_check(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Project Management API is running!', response.get_data(as_text=True))

    def test_login_invalid(self):
        response = self.app.post('/api/auth/login', json={"email": "fake@example.com", "password": "wrong"})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.get_data(as_text=True))


        def test_get_tasks(self):
            response = self.app.get('/api/tasks/')
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, list)

        def test_create_task_missing_fields(self):
            response = self.app.post('/api/tasks/', json={"title": "Test Task"})
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.get_data(as_text=True))

        def test_generate_user_stories_missing_description(self):
            response = self.app.post('/api/ai/generate-user-stories', json={})
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
