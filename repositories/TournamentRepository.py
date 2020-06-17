from domain.Tournament import Tournament
from repositories import UserRepository, PlayerRepository
from psycopg2 import ProgrammingError, DatabaseError
import logging


class TournamentRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def __loadData(self, usersDict, repository):

        userRepository = UserRepository.UserRepository(self.dbConnectionPool)
        playerRepository = PlayerRepository.PlayerRepository(self.dbConnectionPool)

        List = []

        if repository == 1:
            for item in usersDict:
                List.append(userRepository.loadOne({"id": item}))
        elif repository == 2:
            for item in usersDict:
                List.append(playerRepository.loadOne({"id": item}))
        return List

    def loadOne(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, type, date, players, access from TOURNAMENTS WHERE id = %(id)s""",
                    _id)
        tournament = cur.fetchone()

        cur.close()
        self.dbConnectionPool.putconn(connection)

        if tournament:
            return Tournament(tournament[1], tournament[2], tournament[3], self.__loadData(tournament[4], 2),
                              self.__loadData(tournament[5], 1), tournament[0]).__dict__
        else:
            return None

    def loadAll(self):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, type, date, players, access from TOURNAMENTS""")
        tournaments = cur.fetchall()
        tournamentsList = []

        cur.close()
        self.dbConnectionPool.putconn(connection)

        for item in tournaments:
            tournamentsList.append(Tournament(item[1], item[2], item[3], self.__loadData(item[4], 2),
                                              self.__loadData(item[5], 1), item[0]).__dict__)

        return tournamentsList

    def save(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""INSERT INTO TOURNAMENTS (name, type, date, players, access) VALUES (%(name)s, %(type)s, 
            %(date)s, %(players)s, %(access)s)""", data)

        except DatabaseError:
            cur.close()
            self.dbConnectionPool.putconn(connection)
            return None

        else:
            connection.commit()
            cur.close()
            self.dbConnectionPool.putconn(connection)
            return data
