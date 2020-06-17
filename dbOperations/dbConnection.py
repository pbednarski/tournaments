import psycopg2
from psycopg2 import pool


def connectionPool():
    try:
        conn = psycopg2.pool.SimpleConnectionPool(2, 50, user="os.environ['DATABASE_USER']",
                                                  password="os.environ['DATABASE_PASS']",
                                                  host="os.environ['DATABASE_HOST']",
                                                  port="5432",
                                                  database="os.environ['DATABASE_DATA']")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)

    else:
        return conn
