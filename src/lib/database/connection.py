import asyncio
import asyncpg

from lib.config.config import DATABASE_URL

POOL = None

async def create_pool():
    global POOL
    if POOL is None:
        try:
            POOL = await asyncpg.create_pool(
                dsn=DATABASE_URL,
                min_size=1,
                max_size=10
            )
            print("Connection pool created successfully.")
        except Exception as e:
            print(f"Error creating connection pool: {e}")

async def get_connection():
    global POOL
    if POOL is None:
        await create_pool()
    return POOL.acquire() # берет соединение из пула
        # замена realise_connection поскольку asynco with делает это за нас

async def close_pool():
    global POOL
    if POOL:
        await POOL.close()
        print("Connection pool closed.")