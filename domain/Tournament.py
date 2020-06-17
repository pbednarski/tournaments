
class Tournament:
    def __init__(self, name, _type, datetime, players, access, _id=None):
        self.Id = _id
        self.Name = name
        self.Type = _type
        self.Date = datetime
        self.PlayersList = players
        self.Access = access
