from flask import Flask, jsonify, request, abort
from services import UserService, PlayerService, TournamentService
from repositories import UserRepository, PlayerRepository, TournamentRepository
from dbOperations import dbConnection
import os

dbConnectionPool = dbConnection.connectionPool()

userRepository = UserRepository.UserRepository(dbConnectionPool)
userService = UserService.UserService(userRepository)

playerRepository = PlayerRepository.PlayerRepository(dbConnectionPool)
playerService = PlayerService.PlayerService(playerRepository)

tournamentRepository = TournamentRepository.TournamentRepository(dbConnectionPool)
tournamentService = TournamentService.TournamentService(tournamentRepository)


def isLoggedIn(function):
    def check(*args, **kwargs):
        if request.headers.get('uuid'):
            uuid = {"uuid": request.headers.get('uuid')}

            loggedUser = userService.isLoggedIn(uuid)

            if loggedUser is None:
                return jsonify({"result": "You need to login to call that method"})
            else:
                return function(loggedUser, *args, **kwargs)

        else:
            return jsonify({"result": "You need to add token to request"})

    check.__name__ = function.__name__
    return check


app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))


@app.route('/user/', methods=['POST', 'GET'])
@isLoggedIn
def userEndpoint(user):
    if request.method == 'POST':
        _answer = userService.addUser(request.json)

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)

    elif request.method == 'GET':
        _answer = userService.getAllUsers(user)

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)


@app.route('/user/<int:_id>', methods=['GET', 'DELETE', 'PUT', 'POST'])
@isLoggedIn
def userByIdEndpoint(_id):

    if request.method == 'GET':
        _answer = userService.getUser({"id": _id})

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer.__dict__)

    elif request.method == 'DELETE':
        _answer = userService.deleteUser({"id": _id})

        if _answer is None:
            return abort(404)
        else:
            return _answer

    elif request.method == 'PUT':
        data = dict({"id": _id}, **request.json)
        _answer = userService.updateUser(data)

        if _answer is None:
            return abort(404)
        else:
            return _answer


@app.route('/player/', methods=['POST', 'GET'])
@isLoggedIn
def playerEndpoint():
    if request.method == 'POST':
        _answer = playerService.addPlayer(request.json)

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)

    elif request.method == 'GET':
        _answer = playerService.getAllPlayers()

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)


@app.route('/player/<int:_id>', methods=['GET', 'DELETE', 'PUT'])
@isLoggedIn
def playerByIdEndpoint(_id):
    if request.method == 'GET':
        _answer = playerService.getPlayer({"id": _id})

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)

    elif request.method == 'DELETE':
        _answer = playerService.deletePlayer({"id": _id})

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)

    elif request.method == 'PUT':
        data = dict({"id": _id}, **request.json)
        _answer = playerService.updatePlayer(data)

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)


@app.route('/tournament/', methods=['POST', 'GET'])
@isLoggedIn
def tournamentEndpoint():
    if request.method == 'POST':
        _answer = tournamentService.addTournament(request.json)

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)

    elif request.method == 'GET':
        _answer = tournamentService.getAllTournaments()

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)


@app.route('/tournament/<int:_id>', methods=['GET', 'DELETE', 'PUT'])
@isLoggedIn
def tournamentByIdEndpoint(_id):
    if request.method == 'GET':
        _answer = tournamentService.getTournament({"id": _id})

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)

    elif request.method == 'DELETE':
        _answer = tournamentService.deleteTournament({"id": _id})

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)

    elif request.method == 'PUT':
        data = dict({"id": _id}, **request.json)
        _answer = tournamentService.updateTournamen(data)

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)


@app.route('/login/', methods=['POST'])
def loginEndpoint():
    if request.method == 'POST':
        token = userService.loginUser(request.json)

        if token is None:
            return abort(404)
        else:
            return jsonify(token)


@app.route('/logout/', methods=['GET'])
def logoutEndpoint():
    if request.method == 'GET':
        _answer = userService.logoutUser({"uuid": request.headers.get('uuid')})

        if _answer is None:
            return abort(404)
        else:
            return jsonify(_answer)


@app.route('/loggedin/', methods=['GET'])
def whoIsLoggedIn():
    if request.method == 'GET':

        if request.headers.get('uuid'):
            uuid = {"uuid": request.headers.get('uuid')}

            _answer = userService.isLoggedIn(uuid)

            if _answer is None:
                return abort(404)
            else:
                return jsonify(_answer.__dict__)

        else:
            return jsonify({"You need to add token to request": ""})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
