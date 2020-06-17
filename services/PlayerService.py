class PlayerService:
    def __init__(self, playerRepository):
        self.userRepository = playerRepository

    def getPlayer(self, _id):
        userEntity = self.userRepository.loadOne(_id)
        return userEntity

    def getAllPlayers(self):
        usersList = self.userRepository.loadAll()
        return usersList

    def addPlayer(self, data):
        userEntity = self.userRepository.save(data)
        return userEntity

    def deletePlayer(self, _id):
        userEntity = self.userRepository.delete(_id)
        return userEntity

    def updatePlayer(self, data):
        userEntity = self.userRepository.update(data)
        return userEntity
