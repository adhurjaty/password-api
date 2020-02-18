import unittest
import uuid

from game import Game
from player import Player
from round import Round
from team import Team

def make_sample_game():
    rounds = [Round(0) for _ in range(5)]
    for r in rounds:
        r.set_word('blah')
    players = [
        Player('Jordan'),
        Player('York'),
        Player('Brittany'),
        Player('Airin'),
    ]
    teams = [
        Team(players[:2]),
        Team(players[2:])
    ]
        
    rounds[0].turn = 1
    rounds[0].score = 6

    rounds[1].turn = 0
    rounds[1].score = 3

    rounds[2].turn = 0
    rounds[2].score = 4

    rounds[3].turn = 1
    rounds[3].score = 5

    rounds[4].turn = 1
    rounds[4].score = 6
    
    game = Game(teams)
    game.rounds = rounds

    return game


class LogicTest(unittest.TestCase):
    def test_get_score(self):
        game = make_sample_game()

        score = game.get_score()
        self.assertEqual(score[0], 7)
        self.assertEqual(score[1], 11)

    def test_get_game_json(self):
        game = make_sample_game()

        player = game.teams[0].players[0]
        obj = game.to_json(player.id)

        self.assertDictEqual(obj, {
            'word': 'blah',
            'turn': 1,
            'pending_score': 6,
            'teams': [
                'Jordan + York',
                'Brittany + Airin'
            ],
            'score': [7, 11]
        })