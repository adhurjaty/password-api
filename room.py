from datetime import datetime
import random
from string import ascii_lowercase

from game import Game


class Room:
    game = None

    def __init__(self):
        self.id = self.generate_id()
        self.created_time = datetime.now()
    
    def generate_id(self):
        return ''.join(random.choice(ascii_lowercase) for _ in range(4))

    def start_game(self, teams):
        self.game = Game(teams)


