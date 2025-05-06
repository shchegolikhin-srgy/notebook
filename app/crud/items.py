import asyncpg
from app.db.base import pool
from app.schemas.items import Task

async def getTasks(userId):
    async with pool.acquire() as conn:
        result=await conn.fetch("SELECT text, completed FROM tasks  WHERE user_id = %i;", (userId))
        return result

async def addTask(task:Task, userId):
    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO tasks (text, completed, user_id) VALUES (%s, %b, %i);", (
            task.text,
            false,
            userId
        ))

async def deleteTask(task:Task, userId):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM tasks WHERE text =%s AND user_id = %i;", (
            task.text, 
            userId
        ))

async def updateTask(task:Task, userId):
    async with pool.acquire() as conn:
        await conn.execute("UPDATE tasks SET text = 'text 2' WHERE text =%s AND user_id = %i;", (
            task.text, 
            userId
        ))
