import asyncpg
from app.db.database import get_db_connection
from app.schemas.items import Task, UpdateTask, ReadTask
from typing import List

async def get_tasks(username:str)-> List[ReadTask]:
    async with get_db_connection() as connection:
        try:
            rows=await connection.fetch("""SELECT tasks.text, tasks.completed
                FROM tasks
                JOIN users ON tasks.user_id = users.id
                WHERE users.username =$1;""",
                "sergey"
            )
            tasks = [ReadTask(text=row['text'], isCompleted=row['completed']) for row in rows]
            return tasks
        except Exception as e:
            return []
        
async def add_task(task:Task, username:str):
    async with get_db_connection() as connection:
        await connection.execute("INSERT INTO tasks (text, completed, user_id) SELECT $1, $2, users.id FROM users WHERE users.username = $3;", 
            task.text,
            task.isCompleted,
            username
        )

async def delete_task(task:Task, username:str = "1234"):
    async with get_db_connection() as connection:
        await connection.execute("DELETE FROM tasks  USING users WHERE tasks.text =$1 AND tasks.user_id = users.id AND users.username = $2;",
            task.text, 
            username
        )

async def update_task(task:UpdateTask, username:str = "1234"):
    async with get_db_connection() as connection:
        await connection.execute("UPDATE tasks SET text = $1 FROM users WHERE tasks.text =$2 AND tasks.user_id = users.id AND users.username = $3;", 
            task.newText,
            task.text, 
            username
        )

async def toggle_complete_task(task:Task):
    async with get_db_connection() as connection:
        await connection.execute("UPDATE tasks SET completed =$1 WHERE text =$2 AND user_id = $3;", 
            not task.isCompleted,
            task.text, 
            task.userID
        )
