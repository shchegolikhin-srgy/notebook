import asyncpg
from app.db.base import get_db_connection
from app.schemas.items import Task, UpdateTask

async def get_tasks(userId):
    async with get_db_connection() as connection:
        result=await connection.fetch("SELECT text, completed FROM tasks  WHERE user_id = $1;", userId)
        return result

async def add_task(task:Task):
    async with get_db_connection() as connection:
        await connection.execute("INSERT INTO tasks (text, completed, user_id) VALUES ($1, $2, $3);", 
            task.text,
            task.isCompleted,
            task.userId
        )
        return {"status": "success"}

async def delete_task(task:Task):
    async with get_db_connection() as connection:
        await connection.execute("DELETE FROM tasks WHERE text =$1 AND user_id = $2;",
            task.text, 
            task.userId
        )
        return { "status": "success"}

async def update_task(task:UpdateTask):
    async with get_db_connection() as connection:
        await connection.execute("UPDATE tasks SET text = $1 WHERE text =$2 AND user_id = $3;", 
            task.newText,
            task.text, 
            task.userId
        )
        return { "status": "success"}

async def toggle_complete_task(task:Task):
    async with get_db_connection() as connection:
        await connection.execute("UPDATE tasks SET completed =$1 WHERE text =$2 AND user_id = $3;", 
            not task.isCompleted,
            task.text, 
            task.userId
        )
        return { "status": "success"}
