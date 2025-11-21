import psycopg2
from ..config.config import db_pool

class UserAlreadyExistsError(Exception):
    pass

def add_user(name: str, email: str, age: int = None) -> int:   # добавить юзера и глянуть айди
    sql = 'INSERT INTO users(name, email, age) VALUES (%s, %s, %s) RETURNING id;'
    connection = db_pool.get_connection()
    if not connection:
        raise ConnectionError('Could not connect to database')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (name, email, age))
            user_id = int(cursor.fetchone()[0])
            connection.commit()
            return user_id
    except psycopg2.IntegrityError:
            connection.rollback()
            raise UserAlreadyExistsError(f'User with email "{email}" already exists')
    finally:
        db_pool.release_connection(connection)

def find_users_by(user_id: int = None, name: str = None) -> list[dict]: # найти юзера
    sql_query = 'SELECT id, name, email, age, is_active, created_at FROM users'
    params = ()

    if user_id:
        sql_query += 'WHERE id = %s'
        params = (user_id,)
    elif name:
        sql_query += 'WHERE name = %s'
        params = (name,)

    connection = db_pool.get_connection()
    if not connection:
        raise ConnectionError('Could not connect to database')

    try:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql_query, params)
            users = cursor.fetchall()
            return [dict(row) for row in users]
    finally:
        db_pool.release_connection(connection)

def update_user(user_id: int, updates: dict) -> int: # обновить юзера и посмотреть что обновилось
    if not updates:
        return 0
    set_clauses = [f'{key} = %s' for key in updates.keys()]
    sql = f'UPDATE users SET {", ".join(set_clauses)} WHERE id = %s;'
    params = list(updates.values() + [user_id])

    connection = db_pool.get_connection()
    if not connection:
        raise ConnectionError('Could not connect to database')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, tuple(params))
            connection.commit()
            return cursor.rowcount
    except psycopg2.IntegrityError:
        connection.rollback()
        raise UserAlreadyExistsError(f'User with this email already exists')
    finally:
        db_pool.release_connection(connection)

def delete_user(user_id: int) -> int: # удаление !!!
    sql = f'DELETE FROM users WHERE id = %s;'
    connection = db_pool.get_connection()
    if not connection:
        raise ConnectionError('Could not connect to database')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, user_id)
            connection.commit()
            return cursor.rowcount
    finally:
        db_pool.release_connection(connection)