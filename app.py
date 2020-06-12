from flask import Flask, jsonify, request
import json
from services.UserService import UserService
from repositories.UserRepository import UserRepository

userRepository = UserRepository()
userService = UserService(userRepository)


app = Flask(__name__)


@app.route('/user/', methods=['POST', 'GET'])
def userEndpoint():
    if request.method == 'POST':
        userService.addUser(request.json)
        return request.json
    elif request.method == 'GET':
        return json.dumps(userService.getAllUsers())


@app.route('/user/<int:_id>', methods=['GET', 'DELETE', 'PUT'])
def userByIdEndpoint(_id):
    if request.method == 'GET':
        return json.dumps(userService.getUser({"id": _id}), indent=4)
    elif request.method == 'DELETE':
        return userService.deleteUser({"id": _id})
    elif request.method == 'PUT':
    # i tutaj muszę przekazać 2 zmienne, id usera i body requesta z danymi do zmiany
    # ale za cholere nie wiem jak to zrobić, żeby później mieć to w jednym JSONie
    # i jak to w ogóle powinno wyglądać w praktyce ?s
        return



if __name__ == '__main__':
    app.run(debug=True)
