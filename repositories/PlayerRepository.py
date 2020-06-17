from domain.Player import Player
from psycopg2 import ProgrammingError, DatabaseError
import logging


class PlayerRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def __closeConnection(self, cursor, connection):
        cursor.close()
        self.dbConnectionPool.putconn(connection)

    def __generatePlayerObject(self, player):
        if player:
            return Player(player[1], player[2], player[0]).__dict__
        else:
            return None

    def loadOne(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""Select id, name, lastname from PLAYERS WHERE id = %(id)s""",
                        _id)

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None
        else:
            player = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generatePlayerObject(player)



    def loadAll(self):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""Select id, name, lastname from PLAYERS""")

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            users = cur.fetchall()
            playersList = []

            self.__closeConnection(cur, connection)

            for item in users:
                playersList.append(Player(item[1], item[2], item[0]).__dict__)

            return playersList

    def save(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""INSERT INTO PLAYERS (name, lastname) VALUES (%(name)s, %(lastname)s) returning *""",
                        data)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)
            return None

        else:
            player = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generatePlayerObject(player)

    def delete(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""DELETE FROM PLAYERS WHERE id = %(id)s""", _id)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            count = cur.rowcount
            self.__closeConnection(cur, connection)

            if count == 1:
                return {"Player Deleted.": _id}
            else:
                return None

    def update(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""UPDATE PLAYERS SET name = %(name)s, lastname = %(lastname)s 
                            WHERE id = %(id)s RETURNING *""", data)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            player = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generatePlayerObject(player)
