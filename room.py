from datetime import datetime
import random
from string import ascii_lowercase

from game import Game
from team import Team

MAX_PLAYERS = 4

class Room:
    game = None
    players = []

    def __init__(self):
        self.id = self.generate_id()
        self.created_time = datetime.now()
    
    def generate_id(self):
        return ''.join(random.choice(ascii_lowercase) for _ in range(4))

    def start_game(self, team_player_ids):

        # map the ids to the player objects 
        teamsGroups = [[next((p for p in self.players if pid == p.id)) 
            for pid in player_ids]
            for player_ids in team_player_ids]
        teams = [Team(x) for x in teamsGroups]

        self.game = Game(teams)
        self.game.start_round()

    def add_player(self, player):
        if len(self.players) >= MAX_PLAYERS:
            raise Exception("too many players")

        if next((p for p in self.players if p.name.lower() == player.name.lower()), None):
            raise Exception(f'player name "{player.name}" already exists')

        self.players.append(player)


