from flask import Flask, jsonify, request
import json
from services.UserService import UserService
from repositories.UserRepository import UserRepository

userRepository = UserRepository()
userService = UserService(userRepository)




app = Flask(__name__)


@app.route('/user/', methods=['POST'])
def addUser():
    if request.method == 'POST':
        userService.addUser(request.json)
    return request.json


@app.route('/user/<int:_id>', methods=['GET'])
def getUser(_id):
    return json.dumps(userService.getUser({"id": _id}), indent=4)


@app.route('/user/<int:_id>', methods=['DELETE'])
def dellUser(_id):
    if request.method == 'DELETE':
        return userService.dellUser({"id": _id})


if __name__ == '__main__':
    app.run(debug=True)