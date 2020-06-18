from domain.User import User
from psycopg2 import ProgrammingError, DatabaseError
import logging
import uuid

class UserRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def __closeConnection(self, cursor, connection):
        cursor.close()
        self.dbConnectionPool.putconn(connection)

    def __generateUserObject(self, user):
        if user:
            return User(user[1], user[2], user[3], user[4], user[5], user[0]).__dict__
        else:
            return None

    def loadOne(self, _id):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""Select id, name, email, dateofbirth, password, access from USERS WHERE id = %(id)s""",
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
            cur.execute("""Select id, name, email, dateofbirth, password, access from USERS""")

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            users = cur.fetchall()
            usersList = []

            self.__closeConnection(cur, connection)

            for item in users:
                usersList.append(User(item[1], item[2], item[3], item[4], item[5], item[0]).__dict__)

            return usersList

    def save(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute(
                """INSERT INTO USERS (name, email, dateofbirth, password, access) VALUES (%(name)s, %(email)s, 
                %(dateofbirth)s, %(password)s, %(access)s) RETURNING *""", data)
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
            cur.execute("""UPDATE USERS SET name = %(name)s, email = %(email)s, dateofbirth = %(dateofbirth)s, 
            password = %(password)s, access = %(access)s WHERE id = %(id)s returning *""", data)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)
            return None

        else:
            user = cur.fetchone()
            self.__closeConnection(cur, connection)

            return self.__generateUserObject(user)


    def loginUser(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""Select id, name, email, dateofbirth, password, access from USERS WHERE name = %(name)s 
            and password = %(password)s""", data)
            user = cur.fetchone()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            if user:
                _uuid = str(uuid.uuid4())
                _newdata = dict({"uuid": _uuid}, **self.__generateUserObject(user))

                cur.execute(
                    """INSERT INTO USERLOGGED (uuid, created, expired, userid) VALUES (%(uuid)s, now(), 
                    now() + '30 minute'::interval, %(Id)s) RETURNING *""", _newdata)
                connection.commit()

                return _uuid

    def logoutUser(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""DELETE from userlogged WHERE uuid = %(uuid)s RETURNING * """, data)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:
            user = cur.fetchone()
            self.__closeConnection(cur, connection)

            if user:
                return {"user logged Out": data}
