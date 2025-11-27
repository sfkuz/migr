import psycopg2
from psycopg2 import pool

from lib.config.config import DATABASE_URL

# Singleton уже встроен в питон
try:
    connection_pool = pool.SimpleConnectionPool(
        1, 10, dsn=DATABASE_URL)
except psycopg2.OperationalError as e:
    print(f"error creating connection pool: {e}")
    connection_pool = None

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)