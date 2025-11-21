import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

# Singleton
class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                print("creating the connection pool")
                cls._instance.connection_pool = pool.SimpleConnectionPool(
                    1, 10, dsn=os.getenv('DATABASE_URL')
                )
            except psycopg2.OperationalError as e:
                print(f"error creating connection pool: {e}")
                cls._instance.connection_pool = None
        return cls._instance

    def get_connection(self):
        if self.connection_pool:
            return self.connection_pool.getconn()
        return None

    def release_connection(self, connection):
        if self.connection_pool:
            self.connection_pool.putconn(connection)

db_pool = Config()