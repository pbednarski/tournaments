class TournamentService:
    def __init__(self, tournamentRepository):
        self.tournamentRepository = tournamentRepository

    def getTournament(self, _id):
        tournamentEntity = self.tournamentRepository.loadOne(_id)
        return tournamentEntity

    def getAllTournaments(self):
        tournamentsList = self.tournamentRepository.loadAll()
        return tournamentsList

    def addTournament(self, data):
        self.tournamentRepository.save(data)

    def deleteTournament(self, _id):
        tournamentEntity = self.tournamentRepository.delete(_id)
        return tournamentEntity

    def updateTournamen(self, _id):
        tournamentEntity = self.tournamentRepository.update(_id)
        return tournamentEntity
