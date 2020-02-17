import os
import random

from round import Round

script_path = os.path.dirname(os.path.realpath(__file__))
word_file_path = os.path.join(script_path, 'common-nouns.txt')


class Game(object):
    rounds = []
    teams = []
    team_order = [0, 1, 1, 0]
    order_idx = 0
    
    def __init__(self, teams):
        self.teams = teams

    def start_round(self, word):
        team_up = self.team_order[self.order_idx]
        self.order_idx += 1
        self.order_idx = self.order_idx % 4

        round = Round(word, team_up)
        self.rounds.append(round)

    def has_started(self):
        return len(self.rounds) > 0
        
    def generate_word(self):
        with open(word_file_path, 'r') as f:
            words = (x.strip() for x in f.readlines())
            return random.choice(words)

    def get_score(self):
        scores = [0, 0]
        for round in self.rounds[:-1]:
            scores[round.turn] += round.score
        return scores

    def to_json(self):
        current_round = self.rounds[-1]

        return {
            'word': current_round.word,
            'turn': current_round.turn,
            'pending_score': current_round.score,
            'teams': [
                t.get_name() for t in self.teams
            ],
            'score': self.get_score()
        }

    