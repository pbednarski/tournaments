from domain.Tournament import Tournament
from repositories import UserRepository, PlayerRepository
from psycopg2 import ProgrammingError, DatabaseError
import logging


class TournamentRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def __closeConnection(self, cursor, connection):
        cursor.close()
        self.dbConnectionPool.putconn(connection)

    def __generateTournamentObject(self, tournament):
        if tournament:
            return Tournament(tournament[1], tournament[2], tournament[3], self.__loadData(tournament[4], 2),
                              self.__loadData(tournament[5], 1), tournament[0]).__dict__
        else:
            return None

    def __loadData(self, _dict, repository):

        userRepository = UserRepository.UserRepository(self.dbConnectionPool)
        playerRepository = PlayerRepository.PlayerRepository(self.dbConnectionPool)

        List = []

        if repository == 1:
            for item in _dict:
                user = userRepository.loadOne({"id": item})
                if user:
                    List.append(user)
        elif repository == 2:
            for item in _dict:
                player = playerRepository.loadOne({"id": item})
                if player:
                    List.append(player)
        return List

    def loadOne(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""Select id, name, type, date, players, access from TOURNAMENTS WHERE id = %(id)s""",
                        _id)

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            tournament = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generateTournamentObject(tournament)

    def loadAll(self):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""Select id, name, type, date, players, access from TOURNAMENTS""")

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            tournaments = cur.fetchall()
            tournamentsList = []

        if tournaments:
            for item in tournaments:
                tournamentsList.append(Tournament(item[1], item[2], item[3], self.__loadData(item[4], 2),
                                                  self.__loadData(item[5], 1), item[0]).__dict__)

            self.__closeConnection(cur, connection)

            return tournamentsList

        else:
            self.__closeConnection(cur, connection)

            return None

    def save(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""INSERT INTO TOURNAMENTS (name, type, date, players, access) VALUES (%(name)s, %(type)s, 
            %(date)s, %(players)s, %(access)s) RETURNING * """, data)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            tournament = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generateTournamentObject(tournament)

    def delete(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""DELETE FROM TOURNAMENTS WHERE id = %(id)s """, _id)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            count = cur.rowcount
            if count == 1:
                self.__closeConnection(cur, connection)

                return {"Tournament Deleted.": _id}
            else:
                self.__closeConnection(cur, connection)

                return None

    def update(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""UPDATE TOURNAMENTS SET name = %(name)s, type = %(type)s, 
            date = %(date)s, players = %(players)s, access = %(access)s 
                            WHERE id = %(id)s returning *""", data)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            tournament = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generateTournamentObject(tournament)
