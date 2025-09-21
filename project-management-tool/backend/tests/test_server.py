import unittest
from backend.app import app

class ProjectApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_projects(self):
        response = self.app.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_project_missing_fields(self):
        response = self.app.post('/api/projects/', json={"name": "Test Project"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
