import unittest
from backend.app import app

class UserApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_users(self):
        response = self.app.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_user_missing_fields(self):
        response = self.app.post('/api/users/', json={"name": "Test"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
