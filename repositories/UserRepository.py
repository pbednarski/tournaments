from domain.User import User
from psycopg2 import ProgrammingError, DatabaseError
import logging

class UserRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def __closeConnection(self, cursor, connection):
        cursor.close()
        self.dbConnectionPool.putconn(connection)

    def __generateUserObject(self, user):
        if user:
            return User(user[1], user[2], user[3], user[0]).__dict__
        else:
            return None

    def loadOne(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""Select id, name, password, access from USERS WHERE id = %(id)s""",
                        _id)

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            user = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generateUserObject(user)

    def loadAll(self):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""Select id, name, password, access from USERS""")

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            users = cur.fetchall()
            usersList = []

            self.__closeConnection(cur, connection)

            for item in users:
                usersList.append(User(item[1], item[2], item[3], item[0]).__dict__)

            return usersList

    def save(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute(
                """INSERT INTO USERS (name, password, access) VALUES (%(name)s, %(password)s, %(access)s) RETURNING *""",
                data)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            user = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generateUserObject(user)

    def delete(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""DELETE FROM USERS WHERE id = %(id)s RETURNING *""", _id)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            user = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generateUserObject(user)

    def update(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""UPDATE USERS SET name = %(name)s, password = %(password)s, access = %(access)s 
                            WHERE id = %(id)s returning *""", data)

        except DatabaseError:
            self.__closeConnection(cur, connection)
            return None

        else:
            user = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generateUserObject(user)
