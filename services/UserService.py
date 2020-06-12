

class UserService:
    def __init__(self, userRepository):
        self.userRepository = userRepository

    def getUser(self, data):
        userEntity = self.userRepository.loadOne(data)
        return userEntity

    def getAllUsers(self):
        usersList = self.userRepository.loadAll()
        return usersList

    def addUser(self, data):
        self.userRepository.save(data)

    def deleteUser(self, data):
        userEntity = self.userRepository.delete(data)
        return userEntity

    def updateUser(self, data):
        userEntity = self.userRepository.update(data)
        return userEntity



