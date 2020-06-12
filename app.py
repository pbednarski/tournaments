from flask import Flask, jsonify, request, abort
from services import UserService, PlayerService
from repositories import UserRepository, PlayerRepository
from dbOperations.dbConnection import connect


dbConnection = connect()

userRepository = UserRepository.UserRepository(dbConnection)
userService = UserService.UserService(userRepository)

playerRepository = PlayerRepository.PlayerRepository(dbConnection)
playerService = PlayerService.PlayerService(playerRepository)


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


@app.route('/player/', methods=['POST', 'GET'])
def playerEndpoint():

    if request.method == 'POST':
        playerService.addPlayer(request.json)
        return request.json

    elif request.method == 'GET':
        return jsonify(playerService.getAllPlayers())

@app.route('/player/<int:_id>', methods=['GET', 'DELETE', 'PUT'])
def playerByIdEndpoint(_id):
    if request.method == 'GET':
        answer = playerService.getPlayer({"id": _id})

        if answer is None:
            return abort(404)
        else:
            return jsonify(answer)

    elif request.method == 'DELETE':
        answer = playerService.deletePlayer({"id": _id})

        if answer is None:
            return abort(404)
        else:
            return answer

    elif request.method == 'PUT':
        data = dict({"id": _id}, **request.json)
        answer = playerService.updatePlayer(data)

        if answer is None:
            return abort(404)
        else:
            return answer


if __name__ == '__main__':
    app.run(debug=True)
