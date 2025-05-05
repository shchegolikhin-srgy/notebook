import asyncpg
from database import pool
from schemas_items import Task

async def getTasks(userId):
    async with pool.acquire() as conn:
        row =await conn.fetch(f"SELECT * FROM tasks WHERE user_id= {userId};")

async def createTask(task:Task):
    async with pool.acquire() as conn:
        await conn.execute(f"INSERT INTO tasks(user_id, text, is_completed) VALUES(1, ' Task number i', false);")
