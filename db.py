import os
import argparse
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # находит файл env и делает его переменные доступными, как если бы они были установленны в системе

DATABASE_URL = os.getenv('DATABASE_URL')

# todo class psycopg2.pool.SimpleConnectionPool, https://www.psycopg.org/docs/pool.html
# https://refactoring.guru/design-patterns/singleton just read
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
         return None
     try:
         with connection: #оч полезная штука, менеджер контекста
             with connection.cursor() as cursor:
                 cursor.execute(sql, (name, email, age)) # отправление команды в базу данных. 1-запрос, 2-кортеж
                 user_id = cursor.fetchone()[0] # айди
                 print(f'user "{name}" successfully added from ID: "{user_id}"')
     except psycopg2.IntegrityError: # ошибка вылазит при уже существующем пользователе
         print(f'error: a user with that email already exists')

# get_user_by_id, get_user_by_name
def read_user(user_id=None, name=None, surename=None, subject=None):
    connection = db_connection()
    if connection is None:
        return None
    try:
        with connection.cursor() as cursor:
            # if user_id:       так делать нельзя, плохо работает
            #     cursor.execute('SELECT * FROM users WHERE id=%s;', (user_id,)) # запятая обязательна чтобы python воспринимал это как кортеж
            # elif name:
            #     cursor.execute('SELECT * FROM users WHERE name=%s;', (name,))
            # else:
            #     cursor.execute('SELECT * FROM users ORDER BY id;')
            #
            # users = cursor.fetchall() # забрать ответ
            sql_query = 'SELECT id, name, email, age, is_active, created_at FROM users'
            if user_id:
                cursor.exec ute(f'{sql_query} WHERE id=%s;', (user_id,))
            elif name:
                cursor.exec ute(f'{sql_query} WHERE name=%s;', (name,))
            else:
                cursor.exec ute(f'{sql_query} ORDER BY id;')

            users = cursor.fetchall()

            if not users:
                print('user not found')
                return None
            print(f"{'ID':<5}{'NAME':<20}{'EMAIL':<30}{'AGE':<5}{'ACTIVE':<10}{'CREATED AT':<20}")
            print('-'*90)
            for user in users:
                user_id, name, email, age, is_active, created_at = user
                age_display = age if age is not None else ''
                print(f"{user_id:<5}{name:<20}{email:<30}{str(age_display):<5}{str(is_active):<10}{created_at.strftime('%Y-%m-%d %H:%M'):<20}")
    finally:
        connection.close()

def update_user(user_id, new_name=None, new_email=None, is_active=None, age=None):
    updates = []
    params = []
    if new_name:
        updates.append('name = %s')
        params.append(new_name)
    if new_email:
        updates.append('email = %s')
        params.append(new_email)
    if is_active is not None:
        updates.append() # todo почему пусто?
        params.append(is_active)
    if age is not None:
        updates.append('age = %s')
        params.append(age)
    if not updates:
        print('no updates')
        return None

    params.append(user_id)

    sql = f'UPDATE users SET {','.join(updates)} WHERE id=%s;'
    connection = db_connection()
    if connection is None:
        return None
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(params))
                if cursor.rowcount == 0:   # проверка вытянутых строк
                    print(f'user from ID {user_id} not found')
                else:
                    print(f'user from ID {user_id} successfully updated')
    except psycopg2.IntegrityError:
        print(f'user from ID {user_id} already exists')
    finally:
        connection.close()

def delete_user(user_id):
    sql = f'DELETE FROM users WHERE id=%s;'
    connection = db_connection()
    if connection is None:
        return None
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id,))
            if cursor.rowcount == 0:
                print(f'user from ID {user_id} not found')
            else:
                print(f'user from ID {user_id} successfully deleted')
    connection.close()

def main():
    parser = argparse.ArgumentParser(description='Database manipulation')
    subparsers = parser.add_subparsers(dest = 'command', help = 'available commands')

    #add
    parser_add = subparsers.add_parser('add', help='add a new user')
    parser_add.add_argument('--name', type=str, required=True, help='user name')
    parser_add.add_argument('--email', type=str, required=True, help='email address')
    parser_add.add_argument('--age', type=int, help='age user')

    #read
    parser_get = subparsers.add_parser('read', help='read a user')
    parser_get.add_argument('--id', type=int, help='ID user to read')
    parser_get.add_argument('--name', type=str, help='user name to read')

    #update
    parser_update = subparsers.add_parser('update', help='update a user')
    parser_update.add_argument('--id', type=int, required=True, help='ID user to update')
    parser_update.add_argument('--new-name', type=str, help='new user name')
    parser_update.add_argument('--new-email', type=str, help='new email')
    parser_update.add_argument('--is-active', type=lambda x: (str(x).lower() == 'true'), help='status active (true/false)')
    parser_update.add_argument('--age', type=int, help='new age')

    #delete
    parser_delete = subparsers.add_parser('delete', help='delete a user')
    parser_delete.add_argument('--id', type=int, required=True, help='ID user to delete')

    args = parser.parse_args()

    if args.command == 'add':
        add_user(args.name, args.email, args.age)
    elif args.command == 'read':
        read_user(args.id, args.name)
    elif args.command == 'update':
        update_user(args.id, args.new_name, args.new_email, args.is_active, args.age)
    elif args.command == 'delete':
        delete_user(args.id)

if __name__ == '__main__':
    main()

# TODO: 1.имя capitalize(), 2.проверка действительно ли email, 3.проверка возраста 4. разбить функции по разным файлам