import psycopg2.extras
from lib.database.connection import get_connection, release_connection

ALLOWED_FIELDS = {"name", "email", "age", "is_active"} # чтобы проверять правильность введенных значений

class UserAlreadyExistsError(Exception):
    pass

def add_user(name: str, email: str, age: int = None) -> int:   # добавить юзера и глянуть айди
    sql = 'INSERT INTO users(name, email, age) VALUES (%s, %s, %s) RETURNING id;'
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (name, email, age))
            user_id = cursor.fetchone()[0]
            connection.commit()
            return user_id
    except psycopg2.IntegrityError:
            connection.rollback()
            raise UserAlreadyExistsError(f'User with email "{email}" already exists')
    finally:
        release_connection(connection)

def read_user(user_id: int = None, name: str = None) -> list[dict]: # найти юзера
    sql_query = 'SELECT id, name, email, age, is_active, created_at FROM users'
    params = ()

    if user_id is not None:
        sql_query += ' WHERE id = %s'
        params = (user_id,)
    elif name is not None:
        sql_query += ' WHERE name = %s'
        params = (name,)
    connection = get_connection()
    try:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql_query, params)
            return cursor.fetchall()
    finally:
        release_connection(connection)

def update_user(user_id: int, updates: dict) -> int:
    filtered = {k: v for k, v in updates.items() if v is not None}
    if not filtered:
        return 0
    set_clauses = [f"{key} = %s" for key in filtered.keys()]
    sql = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = %s"
    params = list(filtered.values()) + [user_id]
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            connection.commit()
            return cursor.rowcount
    except psycopg2.IntegrityError as e:
        connection.rollback()
        if "users_email_key" in str(e):
            raise UserAlreadyExistsError("Email already exists")
        raise
    finally:
        release_connection(connection)


def delete_user(user_id: int) -> int: # удаление !!!
    sql = f'DELETE FROM users WHERE id = %s;'
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (user_id,))
            connection.commit()
            return cursor.rowcount
    finally:
        release_connection(connection)