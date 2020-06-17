from flask import Flask, jsonify, request, abort
from services import UserService, PlayerService, TournamentService
from repositories import UserRepository, PlayerRepository, TournamentRepository
from dbOperations import dbConnection

dbConnectionPool = dbConnection.connectionPool()

userRepository = UserRepository.UserRepository(dbConnectionPool)
userService = UserService.UserService(userRepository)

playerRepository = PlayerRepository.PlayerRepository(dbConnectionPool)
playerService = PlayerService.PlayerService(playerRepository)

tournamentRepository = TournamentRepository.TournamentRepository(dbConnectionPool)
tournamentService = TournamentService.TournamentService(tournamentRepository)

app = Flask(__name__)


@app.route('/user/', methods=['POST', 'GET'])
def userEndpoint():
    if request.method == 'POST':
        answer = userService.addUser(request.json)

        if answer is None:
            return abort(404)
        else:
            return jsonify(answer)


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


@app.route('/tournament/', methods=['POST', 'GET'])
def tournamentEndpoint():
    if request.method == 'POST':
        tournamentService.addTournament(request.json)
        return request.json

    elif request.method == 'GET':
        return jsonify(tournamentService.getAllTournaments())


@app.route('/tournament/<int:_id>', methods=['GET', 'DELETE', 'PUT'])
def tournamentByIdEndpoint(_id):
    if request.method == 'GET':
        answer = tournamentService.getTournament({"id": _id})

        if answer is None:
            return abort(404)
        else:
            return jsonify(answer)


if __name__ == '__main__':
    app.run(debug=True)

dbConnectionPool.closeall()
