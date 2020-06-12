from flask import Flask, jsonify, request, abort
from services.UserService import UserService
from repositories.UserRepository import UserRepository
from dbOperations.dbConnection import connect

dbConnection = connect()

userRepository = UserRepository(dbConnection)
userService = UserService(userRepository)


app = Flask(__name__)


@app.route('/user/', methods=['POST', 'GET'])
def userEndpoint():

    if request.method == 'POST':
        userService.addUser(request.json)
        return request.json

    elif request.method == 'GET':
        return jsonify(userService.getAllUsers())


@app.route('/user/<int:_id>', methods=['GET', 'DELETE', 'PUT'])
def userByIdEndpoint(_id):
    if request.method == 'GET':
        answer = userService.getUser({"id": _id})

        if answer is None:
            return abort(404)
        else:
            return jsonify(answer)

    elif request.method == 'DELETE':
        answer = userService.deleteUser({"id": _id})

        if answer is None:
            return abort(404)
        else:
            return answer

    elif request.method == 'PUT':
        data = dict({"id": _id}, **request.json)
        answer = userService.updateUser(data)

        if answer is None:
            return abort(404)
        else:
            return answer



if __name__ == '__main__':
    app.run(debug=True)
