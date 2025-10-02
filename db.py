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

def add_user(name, email, age=None):
     sql = ('INSERT INTO users(name, email, age) VALUES(%s, %s, %s) RETURNING id;')
     connection = db_connection()
     if connection is None:
         return
     try:
         with connection: #оч полезная штука, менеджер контекста
             with connection.cursor() as cursor:
                 cursor.execute(sql, (name, email, age)) # отправление команды в базу данных. 1-запрос, 2-кортеж
                 user_id = cursor.fetchone()[0] # айди
                 print(f'user "{name}" successfully added from ID: "{user_id}"')
     except psycopg2.IntegrityError: # ошибка вылазит при уже существующем пользователе
         print(f'error: a user with that email already exists')
     finally:
        connection.close()

def read_user(user_id=None, name=None):
    connection = db_connection()
    if connection is None:
        return
    try:
        with connection.cursor() as cursor:
            if user_id:
                cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,)) # запятая обязательна чтобы python воспринимал это как кортеж
            elif name:
                cursor.execute('SELECT * FROM users WHERE name=%s;', (name,))
            else:
                cursor.execute('SELECT * FROM users ORDER BY id;')

            users = cursor.fetchall() # забрать ответ

            if not users:
                print('user not found')
                return
            print(f'{'ID':<5}{'NAME:<20'}{'EMAIL':<30}{'AGE':<5}{'ACTIVE':<10}{'CREATED AT'}')
            print('-'*85)
            for user in users:
                user_id, name, email, created_at, is_active, age = user
                age_display = age if age is not None else ''
            print(f"{user_id:<5}{name:<20}{email:<30}{str(age_display):<5}{str(is_active):<10}{created_at.strftime('%Y-%m-%d %H:%M')}")
    finally:
        connection.close()

def update_user(user_id, new_name=None, new_email=None, is_active=None, age=None):
    updates = []
    params = []
    