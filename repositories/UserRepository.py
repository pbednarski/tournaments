from domain.User import User
from psycopg2 import ProgrammingError, DatabaseError
from datetime import datetime
import logging
import uuid


def adminCheck(function):
    def check(self, _user, *args, **kwargs):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        if _user.Access == "1":
            result = function(self, _user, cur, connection, *args, **kwargs)
        else:
            result = {"result": "you do not have permissions to proceed."}
        cur.close()
        self.dbConnectionPool.putconn(connection)
        return result

    return check


class UserRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def __generateUserObject(self, user):
        if user:
            return User(user[1], user[2], user[3], user[4], user[5], user[0])
        else:
            return None

    @adminCheck
    def loadOne(self, _user, cur, connection, _id):
        try:
            cur.execute("""Select id, name, email, dateofbirth, password, access from USERS WHERE id = %(id)s""",
                        {"id": _id})
        except DatabaseError:
            return {"result": "Database Execute Error"}
        else:
            user = cur.fetchone()
            return self.__generateUserObject(user).__dict__

    @adminCheck
    def loadAll(self, user, cur, connection):
        try:
            cur.execute("""Select id, name, email, dateofbirth, password, access from USERS""")
        except DatabaseError:
            return {"result": "Database Execute Error"}
        else:
            users = cur.fetchall()
            usersList = []
            for item in users:
                usersList.append(User(item[1], item[2], item[3], item[4], item[5], item[0]).__dict__)
            return usersList

    @adminCheck
    def save(self, _user, cur, connection, data):
        try:
            cur.execute(
                """INSERT INTO USERS (name, email, dateofbirth, password, access) VALUES (%(name)s, %(email)s, 
                %(dateofbirth)s, %(password)s, %(access)s) RETURNING *""", data)
            connection.commit()
        except DatabaseError:
            return {"result": "Database Execute Error"}
        else:
            user = cur.fetchone()
            return self.__generateUserObject(user).__dict__

    @adminCheck
    def delete(self, _user, cur, connection, _id):
        try:
            cur.execute("""DELETE FROM USERS WHERE id = %(id)s RETURNING *""", _id)
            connection.commit()
        except DatabaseError:
            return {"result": "Database Execute Error"}
        else:
            user = cur.fetchone()
            if user:
                return self.__generateUserObject(user).__dict__
            else:
                return {"result": "Database Execute Error"}

    @adminCheck
    def update(self, _user, cur, connection, data):
        try:
            cur.execute("""UPDATE USERS SET name = %(name)s, email = %(email)s, dateofbirth = %(dateofbirth)s, 
            password = %(password)s, access = %(access)s WHERE id = %(id)s returning *""", data)
            connection.commit()
        except DatabaseError:
            return {"result": "Database Execute Error"}
        else:
            user = cur.fetchone()
            if user:
                return self.__generateUserObject(user).__dict__
            else:
                return {"result": "nie udało się uaktualnić użytkownika"}

    def loginUser(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        try:
            cur.execute("""Select id, name, email, dateofbirth, password, access from USERS WHERE name = %(name)s 
            and password = %(password)s""", data)
            user = cur.fetchone()
        except DatabaseError:
            cur.close()
            self.dbConnectionPool.putconn(connection)
            return {"result": "Database Execute Error"}
        else:
            if user:
                _uuid = str(uuid.uuid4())
                try:
                    cur.execute(
                        """INSERT INTO USERLOGGED (uuid, created, expired, userid) VALUES (%(uuid)s, now(), 
                        now() + '90 minute'::interval, %(id)s) RETURNING *""", {"uuid": _uuid, "id": user[0]})
                    connection.commit()
                except DatabaseError:
                    cur.close()
                    self.dbConnectionPool.putconn(connection)
                    return {"result": "User Already Logged in"}
                else:
                    cur.close()
                    self.dbConnectionPool.putconn(connection)
                    return _uuid

    def logoutUser(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        try:
            cur.execute("""DELETE from userlogged WHERE uuid = %(uuid)s RETURNING * """, data)
            connection.commit()
        except DatabaseError:
            cur.close()
            self.dbConnectionPool.putconn(connection)
            return {"Result": "User not Logged in"}
        else:
            user = cur.fetchone()
            cur.close()
            self.dbConnectionPool.putconn(connection)
            if user:
                return {"Result": "user logged Out"}

    def isLoggedIn(self, _uuid):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        try:
            cur.execute("""Delete FROM userlogged where expired < now()""")
            connection.commit()
        except DatabaseError:
            cur.close()
            self.dbConnectionPool.putconn(connection)
            return None
        else:
            try:
                cur.execute("""SELECT id, uuid, created, expired, userid FROM userlogged where uuid = %(uuid)s""",
                            _uuid)
                loggedUser = cur.fetchone()
            except DatabaseError:
                cur.close()
                self.dbConnectionPool.putconn(connection)
                return {"result": "Database Execute Error"}
            else:
                if loggedUser:
                    cur.execute(
                        """Select id, name, email, dateofbirth, password, access from USERS WHERE id = %(id)s""",
                        {"id": loggedUser[4]})
                    user = cur.fetchone()
                    cur.close()
                    self.dbConnectionPool.putconn(connection)
                    return self.__generateUserObject(user)
                else:
                    cur.close()
                    self.dbConnectionPool.putconn(connection)
                    return None
