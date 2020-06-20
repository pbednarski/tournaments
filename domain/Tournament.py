
class Tournament:
    def __init__(self, name, datetime, maxplayers, players, createdby, challengeladder, isactive=False, _id=None):
        self.Id = _id
        self.Name = name
        self.StartingDate = datetime
        self.MaxPlayers = maxplayers
        self.PlayersList = players
        self.CreatedBy = createdby
        self.ChallengeLadder = challengeladder
        self.IsActive = isactive
