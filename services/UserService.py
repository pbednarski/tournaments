from classes.User import User

class UserService:
    def __init__(self, userRepository):
        self.userRepository = userRepository

    def getUser(self, data):
        userEntity = self.userRepository.load(data)
        return userEntity

    def addUser(self, data):
        self.userRepository.save(data)

    def dellUser(self, data):
        userEntity = self.userRepository.delete(data)
        return userEntity
