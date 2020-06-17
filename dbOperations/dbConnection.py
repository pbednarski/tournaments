import psycopg2
from psycopg2 import pool


def connectionPool():
    try:
        conn = psycopg2.pool.SimpleConnectionPool(2, 50, user="process.env.DATABASE_USER",
                                                  password="process.env.DATABASE_PASS",
                                                  host="process.env.DATABASE_HOST",
                                                  port="5432",
                                                  database="process.env.DATABASE_DATA")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)

    else:
        return conn
