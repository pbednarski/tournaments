from dbOperations.dbConnection import connect
from classes.User import User

class UserRepository:
    def __init__(self):
        pass

def load(self, user):
    connection = connect()
    cur = connection.cursor()
    cur.execute('SELECT id, name, type from users where id = %s', user.id)
    data = cur.fetchone()
    cur.close()
    connection.close()
    usernew = User(data[1], data[2])
    return usernew
