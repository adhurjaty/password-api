from round import Round

class Game(object):
    rounds = []
    teams = []
    team_order = [0, 1, 1, 0]
    order_idx = 0
    
    def __init__(self, teams):
        self.teams = teams

    def start_round(self):
        team_up = self.team_order[self.order_idx]
        self.order_idx += 1
        self.order_idx = self.order_idx % 4

        round = Round(team_up)
        self.rounds.append(round)

    def has_started(self):
        return len(self.rounds) > 0
        
    def get_score(self):
        scores = [0, 0]
        for round in self.rounds[:-1]:
            scores[round.turn] += round.score
        return scores

    def set_word(self, word):
        current_round = self.rounds[-1]

        current_round.set_word(word)

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

    def set_correct(self):
        self.start_round()

    def set_incorrect(self):
        current_round = self.rounds[-1]
        current_round.switch_turn()

        if current_round.score == 0:
            self.start_round()
        

    