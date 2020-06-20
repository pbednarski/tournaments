from domain.Tournament import Tournament
from repositories import UserRepository, PlayerRepository
from psycopg2 import ProgrammingError, DatabaseError
import logging


def userCheck(function):
    def check(self, _user, *args, **kwargs):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        if _user:
            result = function(self, _user, cur, connection, *args, **kwargs)
        else:
            result = function(self, _user, cur, connection, *args, **kwargs)
        cur.close()
        self.dbConnectionPool.putconn(connection)
        return result

    return check


class TournamentRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def __generateTournamentObject(self, tournament):
        if tournament:
            return Tournament(tournament[1], tournament[2], tournament[3], tournament[4], tournament[5],
                              tournament[6], tournament[7], tournament[0])

    def __generateAllTournamentsObject(self, tournaments):
        tournamentsList = []
        if tournaments:
            for item in tournaments:
                tournamentsList.append(Tournament(item[1], item[2], item[3], item[4],
                                                  item[5], item[6], item[7], item[0]).__dict__)

            return tournamentsList

    @userCheck
    def loadOne(self, user, cur, connection, _id):
        if user is None:
            try:
                cur.execute("""Select id, name, startingdate, maxplayers, playerslist, createdby, challengeladder, 
                                isactive from TOURNAMENTS WHERE id = %(id)s and isactive = true""", _id)
            except DatabaseError:
                return {"result": "database Error 0"}
            else:
                tournament = cur.fetchone()
                if tournament:
                    return self.__generateTournamentObject(tournament).__dict__
                else:
                    return {"result": "there is no active tournaments"}
        if user.Access == '1':
            try:
                cur.execute("""Select id, name, startingdate, maxplayers, playerslist, createdby, challengeladder, 
                                isactive from TOURNAMENTS WHERE id = %(id)s""", _id)
            except DatabaseError:
                return {"result": "database Error 0"}
            else:
                tournament = cur.fetchone()
                if tournament:
                    return self.__generateTournamentObject(tournament).__dict__
                else:
                    return {"result": "there is no any tournaments"}
        if user.Access == '2':
            try:
                cur.execute("""Select id, name, startingdate, maxplayers, playerslist, createdby, challengeladder, 
                                isactive from TOURNAMENTS WHERE id = %(id)s and createdby = %(userid)s """,
                            dict({"userid": user.Id}, **_id))
            except DatabaseError:
                return {"result": "database Error 0"}
            else:
                tournament = cur.fetchone()
                if tournament:
                    return self.__generateTournamentObject(tournament).__dict__
                else:
                    return {"result": "this is not a tournament created by you"}

    @userCheck
    def loadAll(self, user, cur, connection):
        if user is None:
            try:
                cur.execute("""Select id, name, startingdate, maxplayers, playerslist, createdby, challengeladder, 
                isactive from TOURNAMENTS where isactive = true """)
            except DatabaseError:
                return {"result": "database Error 0"}
            else:
                tournaments = cur.fetchall()
                return self.__generateAllTournamentsObject(tournaments)

        elif user.Access == '1':
            try:
                cur.execute(
                    """Select id, name, startingdate, maxplayers, playerslist, createdby, challengeladder,
                     isactive from TOURNAMENTS""")
            except DatabaseError:
                return {"result": "database Error 1"}
            else:
                tournaments = cur.fetchall()
                return self.__generateAllTournamentsObject(tournaments)

        elif user.Access == '2':
            try:
                cur.execute(
                    """Select id, name, startingdate, maxplayers, playerslist, createdby, challengeladder, 
                    isactive from TOURNAMENTS where createdby = %(userid)s""", {"userid": user.Id})
            except DatabaseError:
                return {"result": "database Error 2"}
            else:
                tournaments = cur.fetchall()
                return self.__generateAllTournamentsObject(tournaments)

    @userCheck
    def save(self, user, cur, connection, data):
        if user is None:
            return {"result": "You do not have permissions to proceed"}
        else:
            try:
                cur.execute("""INSERT INTO TOURNAMENTS (name, startingdate, maxplayers, playerslist, 
                createdby, challengeladder, isactive) VALUES (%(name)s, %(startingdate)s, 
                %(maxplayers)s, %(playerslist)s, %(userid)s, %(challengeladder)s, %(isactive)s) RETURNING * """,
                            dict({"userid": user.Id}, **data))
                connection.commit()

            except (Exception, DatabaseError) as s:
                return {"result": str(s)}

            else:
                tournament = cur.fetchone()
                if tournament:
                    return self.__generateTournamentObject(tournament).__dict__
                else:
                    return {"result": "Tournament wasn't added"}

    @userCheck
    def delete(self, user, cur, connection, _id):
        if user is None:
            return {"result": "You do not have permissions to proceed"}
        else:
            if user.Access == '1':
                try:
                    cur.execute("""DELETE FROM TOURNAMENTS WHERE id = %(id)s RETURNING *""", _id)
                    connection.commit()
                except DatabaseError:
                    return {"result": "database Error 2"}
                else:
                    tournament = cur.fetchone()
                    if tournament:
                        return {"result": {"deleted tournament": self.__generateTournamentObject(tournament).__dict__}}
                    else:
                        return {"result": "Tournament wasn't deleted"}
            elif user.Access == '2':
                try:
                    cur.execute("""DELETE FROM TOURNAMENTS WHERE id = %(id)s and createdby = %(userid)s 
                    isactive = false RETURNING *""", dict({"userid": user.Id}, **_id))
                    connection.commit()
                except DatabaseError:
                    return {"result": "database Error 2"}
                else:
                    tournament = cur.fetchone()
                    if tournament:
                        return {"result": {"deleted tournament": self.__generateTournamentObject(tournament).__dict__}}
                    else:
                        return {"result": "You cannot dellete this tournament. It's not yours or active"}

    @userCheck
    def update(self, user, cur, connection, data):
        if user is None:
            return {"result": "You do not have permissions to proceed"}
        else:
            if user.Access == '1':
                try:
                    cur.execute("""UPDATE TOURNAMENTS SET name = %(name)s, startingdate = %(startingtime)s, 
                    maxplayers = %(maxplayers)s, playerslist = %(playerslist)s, challengeladder = %(challengeladder)s,
                    isactive = %(isactive)s WHERE id = %(id)s returning *""", data)
                    connection.commit()
                except DatabaseError:
                    return {"result": "database Error 2"}
                else:
                    tournament = cur.fetchone()
                    if tournament:
                        return self.__generateTournamentObject(tournament)
                    else:
                        return {"result": "Tournament Entity not updated"}
            elif user.Access == '2':
                try:
                    cur.execute("""UPDATE TOURNAMENTS SET name = %(name)s, startingdate = %(startingtime)s, 
                    maxplayers = %(maxplayers)s, playerslist = %(playerslist)s, challengeladder = %(challengeladder)s,
                    isactive = %(isactive)s WHERE id = %(id)s and createdby = %(userid)s and isactive = false 
                    returning *""", dict({"userid": user.Id}, **data))
                    connection.commit()
                except DatabaseError:
                    return {"result": "database Error 2"}
                else:
                    tournament = cur.fetchone()
                    if tournament:
                        return self.__generateTournamentObject(tournament)
                    else:
                        return {"result": "You cannot edit, this tournament. Its not yours, or it's active"}
