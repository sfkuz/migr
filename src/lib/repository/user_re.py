import asyncpg
from lib.database.connection import get_connection

ALLOWED_FIELDS = {"name", "email", "age", "is_active"}

class UserAlreadyExistsError(Exception):
    pass

async def add_user(name: str, email: str, age: int = None) -> int:
    sql = 'INSERT INTO users(name, email, age) VALUES ($1, $2, $3) RETURNING id;'
    async with await get_connection() as connection:
        try:
            user_id = await connection.fetchval(sql, name, email, age)
            return user_id
        except asyncpg.exceptions.UniqueViolationError:
            raise UserAlreadyExistsError(f'User with email "{email}" already exists')


async def read_user(user_id: int = None, name: str = None) -> list[dict]:
    sql_query = 'SELECT id, name, email, age, is_active, created_at FROM users'
    params = []

    if user_id is not None:
        sql_query += ' WHERE id = $1'
        params.append(user_id)
    elif name is not None:
        sql_query += ' WHERE name = $1'
        params.append(name)

    async with await get_connection() as connection:
        records = await connection.fetch(sql_query, *params)
        return [dict(record) for record in records]

async def update_user(user_id: int, updates: dict) -> int:
    filtered = {k: v for k, v in updates.items() if v is not None}
    if not filtered:
        return 0
    set_clauses = [f"{key} = ${i + 1}" for i, key in enumerate(filtered.keys())]
    sql = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = ${len(filtered) + 1}"
    params = list(filtered.values()) + [user_id]

    async with await get_connection() as connection:
        try:
            status = await connection.execute(sql, *params)
            return int(status.split(' ')[1])
        except asyncpg.exceptions.UniqueViolationError as e:
            if "users_email_key" in str(e):
                raise UserAlreadyExistsError("Email already exists")
            raise


async def delete_user(user_id: int) -> int:
    sql = f'DELETE FROM users WHERE id = $1;'
    async with await get_connection() as connection:
        status = await connection.execute(sql, user_id)
        return int(status.split(' ')[1])