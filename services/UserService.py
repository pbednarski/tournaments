

class UserService:
    def __init__(self, userRepository):
        self.userRepository = userRepository

    def getUser(self, _id):
        userEntity = self.userRepository.loadOne(_id)
        return userEntity

    def getAllUsers(self):
        usersList = self.userRepository.loadAll()
        return usersList

    def addUser(self, data):
        userEntity = self.userRepository.save(data)
        return userEntity

    def deleteUser(self, _id):
        userEntity = self.userRepository.delete(_id)
        return userEntity

    def updateUser(self, data):
        userEntity = self.userRepository.update(data)
        return userEntity



