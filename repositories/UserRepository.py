from domain.User import User
from psycopg2 import ProgrammingError, DatabaseError

class UserRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def loadOne(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, password, access from USERS WHERE id = %(id)s""",
                    _id)
        user = cur.fetchone()

        cur.close()
        self.dbConnectionPool.putconn(connection)

        if user:
            return User(user[1], user[2], user[3], user[0]).__dict__
        else:
            return None

    def loadAll(self):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, password, access from USERS""")
        users = cur.fetchall()
        usersList = []

        cur.close()
        self.dbConnectionPool.putconn(connection)

        for item in users:
            usersList.append(User(item[1], item[2], item[3], item[0]).__dict__)

        return usersList

    def save(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""INSERT INTO USERS (name, password, access) VALUES (%(name)s, %(password)s, %(access)s)""",
                        data)
        except DatabaseError:
            cur.close()
            self.dbConnectionPool.putconn(connection)
            return None

        else:
            connection.commit()
            cur.close()
            self.dbConnectionPool.putconn(connection)
            return data

    def delete(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""DELETE FROM USERS WHERE id = %(id)s """, _id)
        count = cur.rowcount

        connection.commit()

        cur.close()
        self.dbConnectionPool.putconn(connection)

        if count == 1:
            return {"User Deleted.": _id}
        else:
            return None

    def update(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        try:
            cur.execute("""UPDATE USERS SET name = %(name)s, password = %(password)s, access = %(access)s 
                            WHERE id = %(id)s""", data)

        except (Exception, DatabaseError) as error:
            cur.close()
            self.dbConnectionPool.putconn(connection)
            return None

        else:
            connection.commit()
            cur.close()
            self.dbConnectionPool.putconn(connection)
            return data
