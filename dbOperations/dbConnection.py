import psycopg2
from psycopg2 import pool
import os


def connectionPool():
    try:
        conn = psycopg2.pool.SimpleConnectionPool(2, 50, user=os.environ.get('DATABASE_USER', None),
                                                  password=os.environ.get('DATABASE_PASS', None),
                                                  host=os.environ.get('DATABASE_HOST', None),
                                                  port="5432",
                                                  database=os.environ.get('DATABASE_DATA', None))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)

    else:
        return conn
