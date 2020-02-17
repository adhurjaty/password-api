from datetime import datetime
import json
import unittest

from game import Game
from room import Room
import server
from test_logic import make_sample_game

class ServerTests(unittest.TestCase):
    def setUp(self):
        app = server.app
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
        room = Room()
        room.id = 'dddd'
        room.game = make_sample_game()
        room.created_time = datetime(2020, 1, 21)
        server.rooms = [room]

        response = self.app.get('/room/dddd', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        parsed = json.loads(response.data)
        self.assertEqual(parsed['id'], 'dddd')
        self.assertEqual(parsed['game']['word'], 'blah')

    def test_find_room_no_game(self):
        room = Room()
        room.id = 'dddd'
        room.created_time = datetime(2020, 1, 21)
        server.rooms = [room]

        response = self.app.get('/room/dddd', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        parsed = json.loads(response.data)
        self.assertEqual(parsed['id'], 'dddd')

    def test_find_missing_room(self):
        room = Room()
        room.id = 'dddd'
        room.game = make_sample_game()
        room.created_time = datetime(2020, 1, 21)
        server.rooms = [room]

        response = self.app.get('/room/asdf', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_create_room(self):
        response = self.app.post('/room', follow_redirects=True)

        parsed = json.loads(response.data)
        self.assertTrue('id' in parsed)


