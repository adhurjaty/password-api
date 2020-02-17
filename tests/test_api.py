import unittest
import json

from server import app


class ServerTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
    
    def test_invalid_page(self):
        response = self.app.get('/fake_endpoint', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        resp_dict = json.loads(response.data)
        self.assertEqual(resp_dict['Error'], 'page not found')

    def test_find_room(self):
        pass

    def test_find_missing_room(self):
        response = self.app.get('/room/asdf', follow_redirects=True)
        self.assertEqual(response.status_code, 404)


