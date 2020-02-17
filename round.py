class Round:
    word = ''
    turn = 0
    score = 6

    def __init__(self, turn):
        self.turn = turn

    def set_word(self, word):
        self.word = word

    def switch_turn(self):
        self.turn = int(not self.turn)
        self.score -= 1

    def to_json(self):
        return {
            'word': self.word,
            'turn': self.turn,
            'score': self.score
        }