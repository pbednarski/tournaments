from flask import Flask, jsonify, request, abort
from domain import User
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
        uuid = request.headers.get('uuid')
        if uuid:

            loggedUser = userService.isLoggedIn({"uuid": request.headers.get('uuid')})

            if isinstance(loggedUser, User.User):
                return function(loggedUser, *args, **kwargs)
            else:
                return jsonify({"result": "Your Session Expired. Login to proceed."})

        else:
            return function(None, *args, **kwargs)

    check.__name__ = function.__name__
    return check


app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))


@app.route('/user/', methods=['POST', 'GET'])
@isLoggedIn
def userEndpoint(user):
    if request.method == 'POST':
        _answer = userService.addUser(user, request.json)
        return jsonify(_answer)

    elif request.method == 'GET':
        _answer = userService.getAllUsers(user)
        return jsonify(_answer)


@app.route('/user/<int:_id>', methods=['GET', 'DELETE', 'PUT'])
@isLoggedIn
def userByIdEndpoint(user, _id):
    if request.method == 'GET':
        _answer = userService.getUser(user, _id)
        return jsonify(_answer)

    elif request.method == 'DELETE':
        _answer = userService.deleteUser(user, {"id": _id})
        return jsonify(_answer)

    elif request.method == 'PUT':
        _answer = userService.updateUser(user, dict({"id": _id}, **request.json))
        return jsonify(_answer)


@app.route('/player/', methods=['POST', 'GET'])
@isLoggedIn
def playerEndpoint(user):
    if request.method == 'POST':
        _answer = playerService.addPlayer(user, request.json)
        return jsonify(_answer)

    elif request.method == 'GET':
        _answer = playerService.getAllPlayers(user)
        return jsonify(_answer)


@app.route('/player/<int:_id>', methods=['GET', 'DELETE', 'PUT'])
@isLoggedIn
def playerByIdEndpoint(user, _id):
    if request.method == 'GET':
        _answer = playerService.getPlayer(user, {"id": _id})
        return jsonify(_answer)

    elif request.method == 'DELETE':
        _answer = playerService.deletePlayer(user, {"id": _id})
        return jsonify(_answer)

    elif request.method == 'PUT':
        data = dict({"id": _id}, **request.json)
        _answer = playerService.updatePlayer(user, data)
        return jsonify(_answer)


@app.route('/tournament/', methods=['POST', 'GET'])
@isLoggedIn
def tournamentEndpoint(user):
    if request.method == 'POST':
        _answer = tournamentService.addTournament(user, request.json)
        return jsonify(_answer)

    elif request.method == 'GET':
        _answer = tournamentService.getAllTournaments(user)
        return jsonify(_answer)


@app.route('/tournament/<int:_id>', methods=['GET', 'DELETE', 'PUT'])
@isLoggedIn
def tournamentByIdEndpoint(user, _id):
    if request.method == 'GET':
        _answer = tournamentService.getTournament(user, {"id": _id})
        return jsonify(_answer)

    elif request.method == 'DELETE':
        _answer = tournamentService.deleteTournament(user, {"id": _id})
        return jsonify(_answer)

    elif request.method == 'PUT':
        data = dict({"id": _id}, **request.json)
        _answer = tournamentService.updateTournamen(user, data)
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
