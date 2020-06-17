from domain.Player import Player

class PlayerRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def loadOne(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, lastname from PLAYERS WHERE id = %(id)s""",
                    data)
        player = cur.fetchone()

        self.dbConnectionPool.putconn(connection)

        if player:
            return Player(player[1], player[2], player[0]).__dict__
        else:
            return None

    def loadAll(self):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, lastname from PLAYERS""")
        users = cur.fetchall()
        cur.close()
        playersList = []

        self.dbConnectionPool.putconn(connection)

        for item in users:
            playersList.append(Player(item[1], item[2], item[0]).__dict__)

        return playersList

    def save(self, data):
        connection = self.dbConnectionPool.getconn()

        cur = connection.cursor()
        cur.execute("""INSERT INTO PLAYERS (name, lastname) VALUES (%(name)s, %(lastname)s)""",
                    data)
        cur.close()
        connection.commit()

        self.dbConnectionPool.putconn(connection)

    def delete(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""DELETE FROM PLAYERS WHERE id = %(id)s""", data)
        count = cur.rowcount
        connection.commit()

        cur.close()
        self.dbConnectionPool.putconn(connection)

        if count == 1:
            return {"Player Deleted.": data}
        else:
            return None

    def update(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""UPDATE PLAYERS SET name = %(name)s, lastname = %(lastname)s 
                        WHERE id = %(id)s""", data)
        connection.commit()
        count = cur.rowcount

        self.dbConnectionPool.putconn(connection)

        if count == 1:
            return data
        else:
            return None




