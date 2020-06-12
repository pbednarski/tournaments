from domain.User import User
import json

class UserRepository:
    def __init__(self, connection):
        self.dbConnectionPool = connection

    def loadOne(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, password, access from USERS WHERE id = %(id)s""",
                    data)
        user = cur.fetchone()

        if user:
            return User(user[1], user[2], user[3], user[0]).__dict__
        else:
            return None

    def loadAll(self):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, password, access from USERS""")
        users = cur.fetchall()
        cur.close()
        usersList = []

        for item in users:
            usersList.append(User(item[1], item[2], item[3], item[0]).__dict__)

        return usersList

    def save(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""INSERT INTO USERS (name, password, access) VALUES (%(name)s, %(password)s, %(access)s)""",
                    data)
        cur.close()
        connection.commit()

    def update(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""with a as (UPDATE USERS SET name = %(name)s, password = %(password)s, access = %(access)s 
                        WHERE id = %(id)s returning 1) select count(*) from a""", data)
        connection.commit()
        count = cur.fetchone()

        if count[0] == 1:
            return data
        else:
            return None

    def delete(self, data):
        connection = self.dbConnectionPool.getconn()
        cur = connection.cursor()
        cur.execute("""with a as (DELETE FROM USERS WHERE id = %(id)s returning 1)
                                select count(*) from a""", data)
        count = cur.fetchone()
        cur.close()
        connection.commit()
        if count[0] == 1:
            return {"User Deleted.": data}
        else:
            return None


