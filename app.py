from flask import Flask, jsonify
from services.UserService import UserService
from repositories.UserRepository import UserRepository



userRepository = UserRepository()
userService = UserService(userRepository)


app = Flask(__name__)



@app.route('/')
def index():
    userService.getUser()
    return "Works"


if __name__ == '__main__':
    app.run(debug=True)