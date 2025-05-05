import asyncpg
from dotenv import load_dotenv
import os

pool = None
load_dotenv()
async def connectionDB():
    global pool
    pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))

async def closePoolDB():
    await pool.close()