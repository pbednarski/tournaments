class UserService:
    def __init__(self, userRepository):
        self.userRepository = userRepository

    def getUser(self, user):
        userEntity = self.userRepository.load(user.id)
        return userEntity