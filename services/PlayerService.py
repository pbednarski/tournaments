class PlayerService:
    def __init__(self, playerRepository):
        self.userRepository = playerRepository

    def getPlayer(self, user, _id):
        userEntity = self.userRepository.loadOne(user, _id)
        return userEntity

    def getAllPlayers(self, user):
        usersList = self.userRepository.loadAll(user)
        return usersList

    def addPlayer(self, user, data):
        userEntity = self.userRepository.save(user, data)
        return userEntity

    def deletePlayer(self, user, _id):
        userEntity = self.userRepository.delete(user, _id)
        return userEntity

    def updatePlayer(self, user, data):
        userEntity = self.userRepository.update(user, data)
        return userEntity
