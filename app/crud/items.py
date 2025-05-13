import asyncpg
from app.db.base import get_db_connection
from app.schemas.items import Task, UpdateTask, ReadTask
from typing import List

async def get_tasks(userID:int)-> List[ReadTask]:
    async with get_db_connection() as connection:
        try:
            rows=await connection.fetch("SELECT text, completed FROM tasks  WHERE user_id = $1;",
                userID
            )
            tasks = [ReadTask(text=row['text'], isCompleted=row['completed']) for row in rows]
            return tasks
        except Exception as e:
            return []
        
async def add_task(task:Task):
    async with get_db_connection() as connection:
        await connection.execute("INSERT INTO tasks (text, completed, user_id) VALUES ($1, $2, $3);", 
            task.text,
            task.isCompleted,
            task.userID
        )
        return {"status": "success"}

async def delete_task(task:Task):
    async with get_db_connection() as connection:
        await connection.execute("DELETE FROM tasks WHERE text =$1 AND user_id = $2;",
            task.text, 
            task.userID
        )
        return { "status": "success"}

async def update_task(task:UpdateTask):
    async with get_db_connection() as connection:
        await connection.execute("UPDATE tasks SET text = $1 WHERE text =$2 AND user_id = $3;", 
            task.newText,
            task.text, 
            task.userID
        )
        return { "status": "success"}

async def toggle_complete_task(task:Task):
    async with get_db_connection() as connection:
        await connection.execute("UPDATE tasks SET completed =$1 WHERE text =$2 AND user_id = $3;", 
            not task.isCompleted,
            task.text, 
            task.userID
        )
        return { "status": "success"}
