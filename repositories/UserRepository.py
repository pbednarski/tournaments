from dbOperations.dbConnection import connect
from classes.User import User
from psycopg2 import ProgrammingError, OperationalError, errorcodes, errors

class UserRepository:
    def __init__(self):
        pass

    @staticmethod
    def load(data):
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

    @staticmethod
    def save(data):
        connection = connect().getconn()
        cur = connection.cursor()
        cur.execute("""INSERT INTO USERS (name, password, access) VALUES (%(name)s, %(password)s, %(access)s)""",
                    data)
        cur.close()
        connection.commit()

    @staticmethod
    def delete(data):
        connection = connect().getconn()
        cur = connection.cursor()
        cur.execute("""with a as (DELETE FROM USERS WHERE id = %(id)s returning 1)
                                select count(*) from a""", data)
        count = cur.fetchone()
        cur.close()
        connection.commit()
        return {"Deleted rows": count[0]}


