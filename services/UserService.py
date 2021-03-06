

class UserService:
    def __init__(self, userRepository):
        self.userRepository = userRepository

    def getUser(self, user, _id):
        userEntity = self.userRepository.loadOne(user, _id)
        return userEntity

    def getAllUsers(self, user):
        usersList = self.userRepository.loadAll(user)
        return usersList

    def addUser(self, user, data):
        userEntity = self.userRepository.save(user, data)
        return userEntity

    def deleteUser(self, user, _id):
        userEntity = self.userRepository.delete(user, _id)
        return userEntity

    def updateUser(self, user, data):
        userEntity = self.userRepository.update(user, data)
        return userEntity

    def loginUser(self, data):
        _uuid = self.userRepository.loginUser(data)
        return _uuid

    def logoutUser(self, data):
        message = self.userRepository.logoutUser(data)
        return message

    def isLoggedIn(self, data):
        userEntity = self.userRepository.isLoggedIn(data)
        return userEntity
