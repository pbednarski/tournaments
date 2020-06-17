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
        tournamentEntity = self.tournamentRepository.save(data)
        return tournamentEntity

    def deleteTournament(self, _id):
        tournamentEntity = self.tournamentRepository.delete(_id)
        return tournamentEntity

    def updateTournamen(self, data):
        tournamentEntity = self.tournamentRepository.update(data)
        return tournamentEntity
