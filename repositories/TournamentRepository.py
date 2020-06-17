from domain.Tournament import Tournament
from psycopg2 import ProgrammingError, DatabaseError


class TournamentRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def loadOne(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, type, date, players, access from TOURNAMENTS WHERE id = %(id)s""",
                    _id)
        tournament = cur.fetchone()

        cur.close()
        self.dbConnectionPool.putconn(connection)

        if tournament:
            return Tournament(tournament[1], tournament[2], tournament[3], tournament[4],
                              tournament[5], tournament[0]).__dict__
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
            tournamentsList.append(Tournament(item[1], item[2], item[3], item[4], item[5], item[0]).__dict__)

        return tournamentsList
