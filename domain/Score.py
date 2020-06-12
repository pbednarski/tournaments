class Score:
    def __init__(self, tournament, player1, player2, score1, score2, datetime, id = None):
        self.Id = id
        self.Tournament = tournament
        self.PlayerOne = player1
        self.PlayerTwo = player2
        self.ScorePlayerOne = score1
        self.ScorePlayerTwo = score2
        self.Date = datetime