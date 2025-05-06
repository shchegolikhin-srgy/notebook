import asyncpg
from app.core.config import DATABASE_URL

pool = None
async def connectionDB():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

async def closePoolDB():
    await pool.close()