from domain.User import User
from psycopg2 import ProgrammingError, DatabaseError
from datetime import datetime
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
            return User(user[1], user[2], user[3], user[4], user[5], user[0])
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

    def loadAll(self, user):

        if user.Access == "1":

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

        else:

            return {"result": "You are not allowed to get users list"}

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
                _newdata = {"uuid": _uuid, "id": user[0]}

                try:
                    cur.execute(
                        """INSERT INTO USERLOGGED (uuid, created, expired, userid) VALUES (%(uuid)s, now(), 
                        now() + '30 minute'::interval, %(id)s) RETURNING *""", _newdata)
                    connection.commit()

                except DatabaseError:
                    self.__closeConnection(cur, connection)

                    return {"User Already Logged in": ""}

                else:
                    self.__closeConnection(cur, connection)

                    return _uuid

    def logoutUser(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""DELETE from userlogged WHERE uuid = %(uuid)s RETURNING * """, data)
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return {"User not Logged in": ""}

        else:
            user = cur.fetchone()
            self.__closeConnection(cur, connection)

            if user:
                return {"user logged Out": data}

    def isLoggedIn(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()

        try:
            cur.execute("""Delete FROM userlogged where expired < now()""")
            connection.commit()

        except DatabaseError:
            self.__closeConnection(cur, connection)

            return None

        else:

            try:
                cur.execute("""SELECT id, uuid, created, expired, userid FROM userlogged where uuid = %(uuid)s""", data)
                loggedUser = cur.fetchone()

            except DatabaseError:
                self.__closeConnection(cur, connection)

                return None

            else:
                if loggedUser:
                    user = self.loadOne({"id": loggedUser[4]})

                    self.__closeConnection(cur, connection)

                    return user
                else:
                    self.__closeConnection(cur, connection)

                    return None
