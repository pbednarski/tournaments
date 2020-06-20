from domain.Player import Player
from psycopg2 import ProgrammingError, DatabaseError
import logging


def userCheck(function):
    def check(self, _user, *args, **kwargs):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        if _user.Access == "1" or _user.Access == "2":
            result = function(self, _user, cur, connection, *args, **kwargs)
        else:
            result = {"result": "you do not have permissions to proceed."}
        cur.close()
        self.dbConnectionPool.putconn(connection)
        return result

    return check


class PlayerRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def __generatePlayerObject(self, player):
        if player:
            return Player(player[1], player[2], player[3], player[0])
        else:
            return None

    @userCheck
    def loadOne(self, _user, cur, connection, _id):
        try:
            cur.execute("""Select id, name, lastname, createdby from PLAYERS WHERE id = %(id)s""", _id)
        except DatabaseError:
            return {"result": "Database Error"}
        else:
            player = cur.fetchone()
            if player:
                return self.__generatePlayerObject(player).__dict__
            else:
                return {"result": "Database Error"}

    @userCheck
    def loadAll(self, user, cur, connection):
        try:
            cur.execute("""Select id, name, lastname, createdby from PLAYERS""")
        except DatabaseError:
            return {"result": "Database Error"}
        else:
            users = cur.fetchall()
            playersList = []
            for item in users:
                playersList.append(Player(item[1], item[2], item[3], item[0]).__dict__)
            return playersList

    @userCheck
    def save(self, user, cur, connection, data):
        try:
            cur.execute("""INSERT INTO PLAYERS (name, lastname, createdby) VALUES (%(name)s, %(lastname)s, 
            %(userid)s) returning *""", dict({"userid": user.Id}, **data))
            connection.commit()
        except DatabaseError:
            return {"result": "Database Error"}
        else:
            player = cur.fetchone()
            return self.__generatePlayerObject(player).__dict__

    @userCheck
    def delete(self, user, cur, connection, _id):
        try:
            cur.execute("""DELETE FROM PLAYERS WHERE id = %(id)s RETURNING *""", _id)
            connection.commit()
        except DatabaseError:
            return {"result": "Database Error"}
        else:
            player = cur.fetchone()
            if player:
                return {"result": {"deleted player": self.__generatePlayerObject(player).__dict__}}
            else:
                return {"result": "Database Error"}

    @userCheck
    def update(self, user, cur, connection, data):
        try:
            cur.execute("""UPDATE PLAYERS SET name = %(name)s, lastname = %(lastname)s 
                            WHERE id = %(id)s RETURNING *""", data)
            connection.commit()
        except DatabaseError:
            return {"result": "Database Error"}
        else:
            player = cur.fetchone()
            if player:
                return {"result": {"updated player": self.__generatePlayerObject(player).__dict__}}
            else:
                return {"result": "Database Error"}
