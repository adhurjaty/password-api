class Team:
    def __init__(self, players):
        self.players = players

    def get_name(self):
        return ' + '.join((p.name for p in self.players))
