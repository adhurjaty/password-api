class Team:
    def __init__(self, players):
        self.players = sorted(players, key=lambda p: p.name)

    def get_name(self):
        return ' + '.join((p.name for p in self.players))
