import asyncpg
from app.db.database import get_db_connection
from app.schemas.items import Task, UpdateTask, DeleteTask
from typing import List
from app.schemas.token import TokenData

async def get_tasks(current_user: TokenData)-> List[Task]:
    async with get_db_connection() as connection:
        try:
            rows=await connection.fetch("""SELECT tasks.text, tasks.completed
                FROM tasks
                JOIN users ON tasks.user_id = users.id
                WHERE users.username =$1;""",
                current_user.username
            )
            tasks = [Task(text=row['text'], isCompleted=row['completed']) for row in rows]
            return tasks
        except Exception:
            return []
        
async def add_task(task:Task, current_user: TokenData):
    async with get_db_connection() as connection:
        await connection.execute("INSERT INTO tasks (text, completed, user_id) SELECT $1, $2, users.id FROM users WHERE users.username = $3;", 
            task.text,
            task.isCompleted,
            current_user.username
        )

async def delete_task(task:DeleteTask, current_user: TokenData):
    async with get_db_connection() as connection:
        await connection.execute("DELETE FROM tasks  USING users WHERE tasks.text =$1 AND tasks.user_id = users.id AND users.username = $2;",
            task.text, 
            current_user.username
        )

async def update_task(task:UpdateTask, current_user: TokenData):
    async with get_db_connection() as connection:
        await connection.execute("UPDATE tasks SET text = $1 FROM users WHERE tasks.text =$2 AND tasks.user_id = users.id AND users.username = $3;", 
            task.newText,
            task.text, 
            current_user.username
        )

async def toggle_complete_task(task:Task, current_user: TokenData):
    async with get_db_connection() as connection:
        await connection.execute("UPDATE tasks SET completed = $1 FROM users WHERE tasks.text =$2 AND tasks.user_id = users.id AND users.username = $3;", 
            task.isCompleted,
            task.text, 
            current_user.username
        )
