import unittest
from app import app

class TestIndex(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_request(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Flask URL Shortener', response.data)

    def test_post_request_valid_url(self):
        response = self.app.post('/', data=dict(url='http://www.example.com'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Copy URL', response.data)
        self.assertIn(b'shortURL', response.data)

if __name__ == '__main__':
    unittest.main()