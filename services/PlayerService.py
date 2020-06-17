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
        self.userRepository.save(data)

    def deletePlayer(self, _id):
        userEntity = self.userRepository.delete(_id)
        return userEntity

    def updatePlayer(self, _id):
        userEntity = self.userRepository.update(_id)
        return userEntity
