class Team:
    def __init__(self, players):
        self.players = players
        self.idx = 0

    def get_name(self):
        return ' + '.join((p.name for p in self.players))

    def get_master(self):
        return self.players[self.idx]

    def get_guesser(self):
        return self.players[int(not self.idx)]

    def switch(self):
        self.idx = int(not self.idx)

    def is_master(self, player_id):
        return self.get_master().id == player_id
