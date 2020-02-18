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

    def to_json(self, player_id):
        current_round = self.rounds[-1]

        data = {
            'turn': current_round.turn,
            'pending_score': current_round.score,
            'teams': [
                t.get_name() for t in self.teams
            ],
            'score': self.get_score()
        }

        if self.is_master(player_id):
            data.update(dict(word=current_round.word))

        return data

    def set_correct(self):
        self.switch_guessers()
        self.start_round()

    def set_incorrect(self):
        current_round = self.rounds[-1]
        current_round.switch_turn()

        if current_round.score == 0:
            self.switch_guessers()
            self.start_round()

    def switch_guessers(self):
        for team in self.teams:
            team.switch()
        
    def is_master(self, player_id):
        return any(team.is_master(player_id) for team in self.teams)    