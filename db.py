import os
import argparse
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # находит файл env и делает его переменные доступными, как если бы они были установленны в системе

DATABASE_URL = os.getenv('DATABASE_URL')

def db_connection():  # конект с бд
    try:
        connection = psycopg2.connect(DATABASE_URL)
        return connection
    except psycopg2.OperationalError as error:
        print(f'database connection error: {error}')
        return None

# CRUD = created, reading, update, deleted

def add_user(name, email, age):
     sql = ('INSERT INTO users(name, email, age) VALUES(%s, %s, %s) RETURNING id;')
     connection = db_connection()
     if connection is None:
         return
     try:
         with connection:
             with connection.cursor() as cursor:
                 cursor.execute(sql, (name, email, age)) # отправление команды в базу данных. 1-запрос, 2-кортеж
                 user_id = cursor.fetchone()[0] # айди
                 print(f'user "{name}" successfully added from ID: "{user_id}"')
     except psycopg2.IntegrityError: # ошибка вылазит при уже существующем пользователе
         print(f'error: a user with that name or email already exists')
     finally:
        connection.close()

