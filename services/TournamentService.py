class TournamentService:
    def __init__(self, tournamentRepository):
        self.tournamentRepository = tournamentRepository

    def getTournament(self, user, _id):
        tournamentEntity = self.tournamentRepository.loadOne(user, _id)
        return tournamentEntity

    def getAllTournaments(self, user):
        tournamentsList = self.tournamentRepository.loadAll(user)
        return tournamentsList

    def addTournament(self, user, data):
        tournamentEntity = self.tournamentRepository.save(user, data)
        return tournamentEntity

    def deleteTournament(self, user, _id):
        tournamentEntity = self.tournamentRepository.delete(user, _id)
        return tournamentEntity

    def updateTournamen(self, user, data):
        tournamentEntity = self.tournamentRepository.update(user, data)
        return tournamentEntity
