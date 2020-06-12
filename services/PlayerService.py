class PlayerService:
    def __init__(self, userRepository):
        self.userRepository = userRepository

    def getPlayer(self, data):
        userEntity = self.userRepository.loadOne(data)
        return userEntity

    def getAllPlayers(self):
        usersList = self.userRepository.loadAll()
        return usersList

    def addPlayer(self, data):
        self.userRepository.save(data)

    def deletePlayer(self, data):
        userEntity = self.userRepository.delete(data)
        return userEntity

    def updatePlayer(self, data):
        userEntity = self.userRepository.update(data)
        return userEntity



