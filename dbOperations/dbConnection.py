import psycopg2
from psycopg2 import pool


def connectionPool():
    try:
        conn = psycopg2.pool.SimpleConnectionPool(2, 50, user="DATABASE_USER",
                                                  password="DATABASE_PASS",
                                                  host="DATABASE_HOST",
                                                  port="5432",
                                                  database="DATABASE_DATABASE")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)

    else:
        return conn

