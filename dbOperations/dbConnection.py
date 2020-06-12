import psycopg2
from psycopg2 import pool


def connect():
    try:
        conn = psycopg2.pool.SimpleConnectionPool(2, 50, user="postgres",
                                                  password="mysecretpassword",
                                                  host="127.0.0.1",
                                                  port="5432",
                                                  database="postgres")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)

    else:
        return conn
