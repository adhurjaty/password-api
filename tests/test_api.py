from datetime import datetime
import json
import unittest

from game import Game
from room import Room
import server
from test_logic import make_sample_game


def add_player(app, name, room_id):
    data = json.dumps(dict(name=name))
    response = app.put(f'/room/{room_id}/add_player', data=data,
        follow_redirects=True)
    parsed = json.loads(response.data)
    return parsed['id']


def create_room(app):
    data = json.dumps(dict(name='Anil'))

    response = app.post('/room', data=data, follow_redirects=True)

    parsed = json.loads(response.data)
    room_id = parsed['id']
    anil_id = parsed['player_id']

    jordan_id = add_player(app, 'Jordan', room_id)
    york_id = add_player(app, 'York', room_id)
    alex_id = add_player(app, 'Alex', room_id)

    teams = [
        [anil_id, jordan_id],
        [york_id, alex_id]
    ]
    
    data = json.dumps(dict(teams=teams))
    response = app.put(f'/room/{anil_id}', data=data,
        follow_redirects=True)

    return anil_id, room_id


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
        self.assertEqual(resp_dict['error'], 'page not found')
    
    def test_create_room(self):
        data = json.dumps(dict(name='Aimee'))
        response = self.app.post('/room', data=data, follow_redirects=True)

        parsed = json.loads(response.data)
        self.assertTrue('id' in parsed)

    def test_find_room(self):
        player_id, room_id = create_room(self.app)

        response = self.app.get(f'/room/{player_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        parsed = json.loads(response.data)
        self.assertEqual(parsed['id'], room_id)

    def test_find_room_game_started(self):
        player_id, room_id = create_room(self.app)

        data = json.dumps(dict(word='blah'))
        self.app.put(f'/room/{player_id}', data=data, follow_redirects=True)

        response = self.app.get(f'/room/{player_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        parsed = json.loads(response.data)
        self.assertEqual(parsed['id'], room_id)
        self.assertEqual(parsed['game']['word'], 'blah')

    def test_find_room_not_master(self):
        player_id, room_id = create_room(self.app)

        data = json.dumps(dict(word='blah'))
        self.app.put(f'/room/{player_id}', data=data, follow_redirects=True)

        server.rooms[0].game.switch_guessers()

        response = self.app.get(f'/room/{player_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        parsed = json.loads(response.data)
        self.assertEqual(parsed['id'], room_id)
        self.assertFalse('word' in parsed['game'])

    def test_find_missing_room(self):
        _, __ = create_room(self.app)

        response = self.app.get('/room/asdf', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_log_correct(self):
        player_id, _ = create_room(self.app)
        game = make_sample_game()

        server.rooms[0].game = game

        data = json.dumps(dict(answer_status='correct'))

        response = self.app.put(f'/room/{player_id}', data=data, follow_redirects=True)
        parsed = json.loads(response.data)

        score = parsed['game']['score']
        pending = parsed['game']['pending_score']

        self.assertListEqual(score, [7, 17])
        self.assertEqual(pending, 6)

    def test_log_incorrect(self):
        player_id, _ = create_room(self.app)
        game = make_sample_game()

        server.rooms[0].game = game

        data = json.dumps(dict(answer_status='incorrect'))

        response = self.app.put(f'/room/{player_id}', data=data, follow_redirects=True)
        parsed = json.loads(response.data)

        score = parsed['game']['score']
        pending = parsed['game']['pending_score']
        turn = parsed['game']['turn']

        self.assertListEqual(score, [7, 11])
        self.assertEqual(pending, 5)
        self.assertEqual(turn, 0)

    def test_incorrect_end_round(self):
        player_id, _ = create_room(self.app)
        game = make_sample_game()

        room = server.rooms[0]
        room.game = game
        room.game.rounds[-1].score = 1
        room.game.rounds[-1].turn = 0

        data = json.dumps(dict(answer_status='incorrect'))

        response = self.app.put(f'/room/{player_id}', data=data, follow_redirects=True)
        parsed = json.loads(response.data)

        score = parsed['game']['score']
        pending = parsed['game']['pending_score']
        turn = parsed['game']['turn']

        self.assertListEqual(score, [7, 11])
        self.assertEqual(pending, 6)
        self.assertEqual(turn, 0)

    def test_start_game(self):
        data = json.dumps(dict(name='Anil'))
        response = self.app.post('/room', data=data, follow_redirects=True)

        parsed = json.loads(response.data)
        room_id = parsed['id']
        anil_id = parsed['player_id']

        jordan_id = add_player(self.app, 'Jordan', room_id)
        york_id = add_player(self.app, 'York', room_id)
        alex_id = add_player(self.app, 'Alex', room_id)

        teams = [
            [anil_id, jordan_id],
            [york_id, alex_id]
        ]
        
        data = json.dumps(dict(teams=teams))
        response = self.app.put(f'/room/{anil_id}', data=data,
            follow_redirects=True)
        
        parsed = json.loads(response.data)

        resp_teams = parsed['game']['teams']
        
        self.assertEqual(parsed['id'], room_id)
        self.assertListEqual(resp_teams, ['Anil + Jordan', 'York + Alex'])

    def test_destroy_room(self):
        _, room_id = create_room(self.app)

        self.assertEqual(len(server.rooms), 1)

        response = self.app.delete(f'/room/{room_id}')

        parsed = json.loads(response.data)

        self.assertEqual(parsed['status'], 'success')
        self.assertEqual(len(server.rooms), 0)