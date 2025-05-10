import asyncpg
from app.core.config import DATABASE_URL
from contextlib import asynccontextmanager

pool = None

async def initialize_db_pool():
    global pool
    try:
        pool = await asyncpg.create_pool(DATABASE_URL)
        if pool:
            print("Database connection pool created successfully.")
    except Exception:
        print(f"Failed to connect to the database: {Exception}")
        raise

async def close_db_pool():
    global pool
    if pool:
        try:
            await pool.close()
        except Exception:
            print(f"Failed to close the database connection pool: {Exception}")

@asynccontextmanager
async def get_db_connection():
    global pool
    if not pool:
        raise HTTPException(status_code=500, detail="Database pool is not initialized")
    async with pool.acquire() as connection:
        yield connection