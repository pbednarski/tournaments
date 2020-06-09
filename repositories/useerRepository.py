from dbOperations.dbConnection import connect

def insertUser(self):
    connection = connect()
    cur = connection.cursor()
    cur.execute("INSERT INTO USERS (name, type) VALUES (%s , %s)", (self.name, self.type))
    cur.close()
    connection.commit()
    connection.close()


def getAllUsers(self):
    connection = connect()
    cur = connection.cursor()
    cur.execute('SELECT id, name, type from users order by id ASC')
    data = cur.fetchall()
    cur.close()
    connection.close()
    return data