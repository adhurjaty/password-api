class Round:
    word = ''
    turn = 0
    score = 6

    def __init__(self, word, turn):
        self.word = word
        self.turn = turn

    def switch_turn(self):
        self.turn = int(not self.turn)
        self.score -= 1