from dbOperations.dbConnection import connect
from domain.User import User

class UserRepository:
    def __init__(self):
        pass

    def loadOne(data):
        connection = connect().getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, password, access from USERS WHERE id = %(id)s""",
                    data)
        user = cur.fetchone()
        cur.close()
        if user:
            return User(user[1], user[2], user[3], user[0]).__dict__
        else:
            return None

    def loadAll(self):
        connection = connect().getconn()
        cur = connection.cursor()
        cur.execute("""Select id, name, password, access from USERS""")
        users = cur.fetchall()
        cur.close()
        usersList = []

        for item in users:
            usersList.append(User(item[1], item[2], item[3], item[0]).__dict__)

        return usersList

    def save(data):
        connection = connect().getconn()
        cur = connection.cursor()
        cur.execute("""INSERT INTO USERS (name, password, access) VALUES (%(name)s, %(password)s, %(access)s)""",
                    data)
        cur.close()
        connection.commit()

    def update(_id, data):
        connection = connect().getconn()
        cur = connection.cursor()
        cur.execute("""with a as (UPDATE USERS SET name = %(name)s, name = %(password)s, name = %(access)s 
        WHERE id = %(id)s returning 1) select count(*) from a""", data)
        count = cur.fetchone()
        cur.close()
        connection.commit()
        if count[0] == 1:
            return data
        else:
            return {"Message": "Unable to update user"}

    def delete(data):
        connection = connect().getconn()
        cur = connection.cursor()
        cur.execute("""with a as (DELETE FROM USERS WHERE id = %(id)s returning 1)
                                select count(*) from a""", data)
        count = cur.fetchone()
        cur.close()
        connection.commit()
        return {"Deleted rows": count[0]}


